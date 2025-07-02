from rest_framework import serializers
from marketplace.models import User, CategorieUser

class CategorieUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategorieUser
        fields = ['id', 'categorie']

class UserSerializer(serializers.ModelSerializer):
    id_categorie_user = CategorieUserSerializer(read_only=True)
    id_categorie_user_id = serializers.PrimaryKeyRelatedField(
        queryset=CategorieUser.objects.all(), source='id_categorie_user', write_only=True
    )
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'justificatif_url',
            'id_categorie_user',
            'id_categorie_user_id',
            'password',
        ]

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)  # hash sécurisé
        user.save()
        return user
