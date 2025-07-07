from django.shortcuts import render
from rest_framework import generics, status, viewsets, permissions, serializers
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


from marketplace.serializers import (
    UserSerializer,
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
    permission_classes = []  # Accès sans authentification

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        # Vérifications rapides des champs obligatoires
        if 'password' not in data or not data['password']:
            return Response({"password": "Ce champ est requis."}, status=status.HTTP_400_BAD_REQUEST)
        if 'id_categorie_user_id' not in data or not data['id_categorie_user_id']:
            return Response({"id_categorie_user_id": "Ce champ est requis."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()  # le hash est géré dans le serializer

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
