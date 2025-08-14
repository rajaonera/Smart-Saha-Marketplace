from rest_framework import viewsets, permissions

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
