from django.core.exceptions import ValidationError
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, SAFE_METHODS
from rest_framework.response import Response

from marketplace.models import (
    Product, Unit, TypePost, Category_Semence, Semence,
)
from marketplace.serializers import (
    ProductSerializer, Category_SemenceSerializers,
)
from marketplace.serializers.Post_serializers import UnitSerializer, TypePostSerializer, SemenceSerializer
from marketplace.views import logger


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

class Category_semenceViewSet(viewsets.ModelViewSet):
    queryset =  Category_Semence.objects.all()
    serializer_class = Category_SemenceSerializers

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        return [IsAuthenticated()]

class SemenceViewSet(viewsets.ModelViewSet):
    queryset = Semence.objects.all()
    serializer_class =  SemenceSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_serializer_context(self):
        return {'request': self.request}

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated], url_path="buy_semence", url_name="buy_semence")
    def buy_semence(self, request):
        semence = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if  serializer.is_valid():
            user  = request.user
            try:
                instance = None
                if semence.user == user:
                    return Response(
                        {'error': 'Vous ne pouvez pas enchérir sur votre propre annonce'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                from psycopg import transaction
                with transaction.atomic():
                    from marketplace.services import Engrais_services
                    instance = Engrais_services.buy_semence(self.request)

                logger.info(f"[Engrais] {user.username} a achete {instance.quantity} sur {semence.name}")

                return Response(
                    {
                        'message': 'Achat placée avec succès',
                        'achat': serializer.data
                    },
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {'error': '[Engrais] achat non valide '},
            status=status.HTTP_400_BAD_REQUEST
        )

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        print("Payload reçu :", request.data)  # Debugging pour vérifier les données reçues
        try:
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        response_serializer = self.get_serializer(instance)
        print("Payload a envoyer :", response_serializer.data)

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

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
