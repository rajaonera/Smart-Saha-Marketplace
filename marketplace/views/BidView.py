from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from django.shortcuts import get_object_or_404

from marketplace.models import Bid, Post
from marketplace.serializers import BidSerializer, BidDetailSerializer
from marketplace.services import cancel_bid,changer_statut,place_bid,update_bid


class BidViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des enchères (Bids)
    - list : Affiche les enchères de l'utilisateur connecté ou d'un post
    - retrieve : Détail d'une enchère
    - partial_update : Modifier une enchère si elle est encore "proposée"
    - destroy : Annuler une enchère (passe au statut "annulée")
    - my_bids : Toutes les enchères de l'utilisateur connecté
    - received_bids : Enchères reçues sur ses annonces
    """
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['post', 'status__name']
    ordering_fields = ['created_at', 'price']
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user
        queryset = Bid.objects.select_related(
            'user', 'post', 'post__user', 'currency'
        ).prefetch_related('status_relations__status')

        post_id = self.request.query_params.get('post_id')
        if post_id:
            post = get_object_or_404(Post, id=post_id)
            if post.user == user:
                return queryset.filter(post=post)  # Propriétaire : toutes les enchères du post
            else:
                return queryset.filter(post=post, user=user)  # Autre : que ses enchères

        return queryset.filter(user=user)  # Sinon : ses propres enchères

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BidDetailSerializer
        return BidSerializer

    def create(self, request, *args, **kwargs):
        """
        Création désactivée ici : utiliser PostViewSet.place_bid à la place
        """
        return Response(
            {"error": "Veuillez utiliser l'endpoint /posts/{id}/place-bid/ pour créer une enchère."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def partial_update(self, request, *args, **kwargs):
        """
        Modification d'une enchère uniquement si statut = "proposée"
        """
        bid = self.get_object()

        if bid.user != request.user:
            return Response(
                {"error": "Vous ne pouvez modifier que vos propres enchères."},
                status=status.HTTP_403_FORBIDDEN
            )

        current_status = bid.get_status_bid()
        if current_status.name.lower() != "proposée":
            return Response(
                {"error": f"Impossible de modifier une enchère avec le statut '{current_status.name}'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with transaction.atomic():
                updated_bid = update_bid(bid, request.data)
                serializer = self.get_serializer(updated_bid)
                return Response(serializer.data)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, *args, **kwargs):
        """
        Annule une enchère (ajoute le statut 'annulée')
        """
        bid = self.get_object()

        if bid.user != request.user:
            return Response(
                {"error": "Vous ne pouvez annuler que vos propres enchères."},
                status=status.HTTP_403_FORBIDDEN
            )

        current_status = bid.get_status_bid()
        if current_status.name.lower() in ["acceptée", "annulée"]:
            return Response(
                {"error": f"Impossible d'annuler une enchère déjà '{current_status.name}'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with transaction.atomic():
                cancel_bid(bid, user=request.user)
                return Response(
                    {"message": "Enchère annulée avec succès."},
                    status=status.HTTP_200_OK
                )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['get'])
    def my_bids(self):
        """
        Retourne toutes les enchères de l'utilisateur connecté
        """
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def received_bids(self, request):
        """
        Enchères reçues sur les annonces (posts) de l'utilisateur connecté
        """
        user = request.user
        queryset = Bid.objects.filter(post__user=user).select_related(
            'user', 'post', 'currency'
        ).prefetch_related('status_relations__status')

        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
