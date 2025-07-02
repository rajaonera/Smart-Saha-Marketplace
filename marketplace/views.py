from django.shortcuts import render
from rest_framework import generics, status, viewsets, permissions, serializers
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from marketplace.models import (
    User, Post, Product, Chat, Message, Review, Favorite, Report, Notification
)
from marketplace.serializers import (
    UserSerializer,
    PostSerializer,
    ProductSerializer,
    ChatSerializer,
    MessageSerializer,
    ReviewSerializer,
    FavoriteSerializer,
    ReportSerializer,
    NotificationSerializer
)

class RegisterRequestSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    id_categorie_user_id = serializers.IntegerField()
    password = serializers.CharField(write_only=True)


@swagger_auto_schema(
    request_body=RegisterRequestSerializer,
    responses={
        201: openapi.Response('Utilisateur créé avec succès'),
        400: 'Requête invalide'
    }
)

class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = []  # Permet l'accès sans authentification

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        # Hash le mot de passe avant sauvegarde
        password = data.pop('password', None)
        if not password:
            return Response({"password": "Ce champ est requis."}, status=status.HTTP_400_BAD_REQUEST)

        # Valide la catégorie utilisateur (par défaut on peut mettre 2 = 'groupe' par exemple)
        categorie_id = data.get('id_categorie_user_id')
        if not categorie_id:
            return Response({"id_categorie_user_id": "Ce champ est requis."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        # Crée le password séparé (table Password) avec hash sécurisé
        from marketplace.models import Password
        hashed_password = make_password(password)
        Password.objects.create(user=user, password=hashed_password)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]  # adapte selon besoin

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

