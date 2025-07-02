from rest_framework import serializers
from marketplace.models import Review, Favorite, Report, User, Post, Message


class ReviewSerializer(serializers.ModelSerializer):
    id_user_from = serializers.PrimaryKeyRelatedField(read_only=True)  # injecté via JWT
    id_user_to = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Review
        fields = [
            'id',
            'id_user_from',
            'id_user_to',
            'rating',
            'comment',
            'created_at',
        ]
        extra_kwargs = {
            'rating': {'min_value': 1, 'max_value': 5},
        }


class FavoriteSerializer(serializers.ModelSerializer):
    id_user = serializers.PrimaryKeyRelatedField(read_only=True)  # injecté via JWT
    id_post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Favorite
        fields = ['id', 'id_user', 'id_post', 'created_at']


class ReportSerializer(serializers.ModelSerializer):
    id_user = serializers.PrimaryKeyRelatedField(read_only=True)  # injecté via JWT
    id_post = serializers.PrimaryKeyRelatedField(
        queryset=Post.objects.all(), required=False, allow_null=True
    )
    id_message = serializers.PrimaryKeyRelatedField(
        queryset=Message.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = Report
        fields = [
            'id',
            'id_user',
            'id_post',
            'id_message',
            'reason',
            'status',
            'created_at',
        ]

    def validate(self, data):
        id_post = data.get('id_post')
        id_message = data.get('id_message')
        if bool(id_post) == bool(id_message):
            raise serializers.ValidationError("Un seul de 'id_post' ou 'id_message' doit être renseigné.")
        return data
