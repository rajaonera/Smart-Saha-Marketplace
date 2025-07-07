from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.db import transaction
from django.utils import timezone
import logging

from marketplace.models import Post, Bid, Bid_status, BidStatusRelation, Post_status
from marketplace.serializers import (
    PostSerializer, PostDetailSerializer, BidSerializer,
    BidDetailSerializer, PlaceBidSerializer
)
from marketplace.models import IsOwnerOrReadOnly

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
        queryset = Post.objects.select_related('user', 'category').prefetch_related('bids')

        status_filter = self.request.query_params.get('status')
        category_filter = self.request.query_params.get('category')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')

        if status_filter:
            queryset = queryset.filter(status__name=status_filter)
        if category_filter:
            queryset = queryset.filter(category__id=category_filter)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset.order_by('-created_at')

    def perform_create(self, serializer):
        """Assigne l'utilisateur connecté lors de la création"""
        serializer.save(user=self.request.user)

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
