from django.core.exceptions import ValidationError
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.db import transaction
from django.utils import timezone
import logging

from marketplace.models import Post, Bid, Bid_status, BidStatusRelation, Post_status, Currency, CategoriePost, \
    PostStatusRelation
from marketplace.serializers import (
    PostSerializer, PostDetailSerializer, BidSerializer,
    BidDetailSerializer, PlaceBidSerializer
)
from marketplace.models import IsOwnerOrReadOnly
from marketplace.serializers.Post_serializers import CurrencySerializer, CategoriePostSerializer, PostStatusSerializer
from rest_framework.decorators import api_view  # Import api_view

logger = logging.getLogger(__name__)  # Ajout d’un logger

class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des annonces (posts)
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_permissions(self):
        """
        Permissions dynamiques selon l'action
        """
        if self.action == 'place_bid':
            return [IsAuthenticated()]
        return super().get_permissions()

    def get_serializer_class(self):
        """Retourne le serializer approprié selon l'action"""
        if self.action == 'retrieve':
            return PostDetailSerializer
        elif self.action == 'place_bid':
            return PlaceBidSerializer
        return PostSerializer

    def get_queryset(self):
        """Filtre les posts selon les paramètres de requête"""
        queryset = Post.objects.select_related(
            'user', 'categorie_post', 'type_post', 'product', 'currency'
        ).prefetch_related(
            'bids', 'labels', 'status'
        )

        status_filter = self.request.query_params.get('status')
        category_filter = self.request.query_params.get('category_post')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        is_published = self.request.query_params.get('is_published')

        if status_filter:
            queryset = queryset.filter(status__name=status_filter)
        if category_filter:
            queryset = queryset.filter(category__id=category_filter)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        if is_published is not None:
            if is_published is True:                
                queryset1 = queryset.filter(status__name='published', is_active=True)
                queryset2 = queryset.filter(status__name='négociation', is_active=True)
                # Combine les queryset pour les posts publiés
                queryset  = queryset1 & queryset2
            else:
                queryset1 = queryset.filter(is_active=False)
                queryset2 = queryset.filter(status__name='brouillon')
                queryset3 = queryset.filter(status__name='supprimé')
                queryset4 = queryset.filter(status__name='vendu')
                # Combine les queryset pour les posts non publiés
                queryset = queryset1 & queryset2 & queryset3 & queryset4
                
        return queryset.order_by('-created_at')

    def perform_create(self, serializer):
        """Assigne l'utilisateur connecté lors de la création"""
        post = serializer.save(user=self.request.user)
        statut = Post_status.objects.get(name="brouillon")
        print("statut", statut.name)
        PostStatusRelation.objects.create(
            post=post,
            status=statut,
            comment="Statut initial"
        )

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def place_bid(self, request):
        """
        Action personnalisée pour placer une enchère sur une annonce
        """
        post = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = request.user
            bid_amount = serializer.validated_data['amount']

            try:
                current_status = post.get_status_post()
                if not current_status or current_status.name.lower() not in ['published', 'négociation']:
                    return Response(
                        {'error': 'Cette annonce n\'accepte pas d\'enchères actuellement'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                if post.user == user:
                    return Response(
                        {'error': 'Vous ne pouvez pas enchérir sur votre propre annonce'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                if bid_amount <= 0:
                    return Response(
                        {'error': 'Le montant de l\'enchère doit être strictement positif'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                if bid_amount <= float(post.price):
                    return Response(
                        {'error': f'L\'enchère doit être supérieure au prix de base ({post.price})'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                existing_bid = Bid.objects.filter(
                    post=post,
                    user=user,
                    status_relations__status__name='proposée'
                ).first()

                if existing_bid:
                    return Response(
                        {'error': 'Vous avez déjà une enchère active sur cette annonce'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                with transaction.atomic():
                    bid = Bid.objects.create(
                        post=post,
                        user=user,
                        amount=bid_amount,
                        message=serializer.validated_data.get('message', ''),
                        created_at=timezone.now()
                    )

                    proposed_status = Bid_status.objects.get(name='proposée')

                    BidStatusRelation.objects.create(
                        bid=bid,
                        status=proposed_status,
                        created_at=timezone.now()
                    )

                    if current_status.name.lower() == 'published':
                        post.changer_statut(Post_status.objects.get(name='négociation'))

                    bid_serializer = BidDetailSerializer(bid)

                    logger.info(f"[Bid] {user.username} a enchéri {bid.price} sur {post.title}")

                    return Response(
                        {
                            'message': 'Enchère placée avec succès',
                            'bid': bid_serializer.data
                        },
                        status=status.HTTP_201_CREATED
                    )

            except Bid_status.DoesNotExist:
                logger.error("[Bid] Statut 'proposée' non configuré")
                return Response(
                    {'error': 'Statut d\'enchère non configuré correctement'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            except Exception as e:
                logger.exception("[Bid] Erreur interne")
                return Response(
                    {'error': f'Erreur interne : {str(e)}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def bids(self, request):
        """
        Récupère toutes les enchères d'une annonce
        """
        post = self.get_object()
        bids = post.bids.select_related('user').prefetch_related('status_relations__status')

        status_filter = request.query_params.get('bid_status')
        if status_filter:
            bids = bids.filter(status_relations__status__name=status_filter)

        serializer = BidSerializer(bids, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def invalidate_posts(self, request):
        """
        Récupère toutes les annonces en brouillon
        """
        posts = Post.objects.filter()
        post = self.get_object()
        bids = post.bids.select_related('user').prefetch_related('status_relations__status')

        status_filter = request.query_params.get('bid_status')
        if status_filter:
            bids = bids.filter(status_relations__status__name=status_filter)

        serializer = BidSerializer(bids, many=True)
        return Response(serializer.data)


    @action (detail=True, methods=['post'])
    def validation_post(self, request):
        post = self.get_object()


class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

class CategoriePostViewSet(viewsets.ModelViewSet):
    queryset = CategoriePost.objects.all()
    serializer_class = CategoriePostSerializer

class PostStatusViewSet(viewsets.ModelViewSet):
    queryset = Post_status.objects.all()
    serializer_class = PostStatusSerializer
    
    # def create(self, request):
    #     serializer = self.get_serializer(data=request.data)
    #     print("Payload reçu :", request.data)  # Debugging pour vérifier les données reçues
    #     try:
    #         serializer.is_valid(raise_exception=True)
    #         instance = serializer.create(request.data)  
    #     except ValidationError as e:
    #         return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    #     response_serializer = self.get_serializer(instance) 
    #     print("Payload a envoyer :", response_serializer.data)  
        
    #     return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        
    
    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
