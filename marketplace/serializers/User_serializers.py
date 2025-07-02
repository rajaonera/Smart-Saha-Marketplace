from rest_framework import serializers
from marketplace.models import User, Password, CategorieUser


class CategorieUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategorieUser
        fields = ['id', 'categorie', 'created_at']


class UserSerializer(serializers.ModelSerializer):
    id_categorie_user = CategorieUserSerializer(read_only=True)
    id_categorie_user_id = serializers.PrimaryKeyRelatedField(
        queryset=CategorieUser.objects.all(), source='id_categorie_user', write_only=True
    )

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'justificatif_url',
            'created_at',
            'id_categorie_user',
            'id_categorie_user_id',
        ]


class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Password
        fields = ['id', 'user', 'password', 'created_at']
        extra_kwargs = {'password': {'write_only': True}}
