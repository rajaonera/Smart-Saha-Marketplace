from django.shortcuts import render
from rest_framework import generics, status, viewsets, permissions, serializers
from rest_framework.permissions import SAFE_METHODS
from rest_framework.permissions import IsAuthenticated, AllowAny

from marketplace.models import (
    User,
)
from marketplace.serializers import (
    UserSerializer,
)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]  # adapte selon besoin

