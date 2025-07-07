from django.shortcuts import render
from rest_framework import generics, status, viewsets, permissions, serializers
from rest_framework.permissions import SAFE_METHODS
from rest_framework.permissions import IsAuthenticated, AllowAny

from marketplace.models import (
     Product,
)
from marketplace.serializers import (
    ProductSerializer,
)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:  # GET, HEAD, OPTIONS
            return [AllowAny()]  # accès libre pour la lecture
        return [IsAuthenticated()]  # POST, PUT, PATCH, DELETE besoin d'être connecté

