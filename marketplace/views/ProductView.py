from typing import Type

from django.shortcuts import render
from rest_framework import generics, status, viewsets, permissions, serializers
from rest_framework.permissions import SAFE_METHODS
from rest_framework.permissions import IsAuthenticated, AllowAny

from marketplace.models import (
    Product, Unit, TypePost,
)
from marketplace.serializers import (
    ProductSerializer,
)
from marketplace.serializers.Post_serializers import UnitSerializer, TypePostSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:  # GET, HEAD, OPTIONS
            return [AllowAny()]  # accès libre pour la lecture
        return [IsAuthenticated()]  # POST, PUT, PATCH, DELETE besoin d'être connecté

class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        return [IsAuthenticated()]


class TypePostViewSet(viewsets.ModelViewSet):
    queryset = TypePost.objects.all()
    serializer_class = TypePostSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        return [IsAuthenticated()]