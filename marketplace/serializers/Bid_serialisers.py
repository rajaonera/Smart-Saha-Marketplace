from rest_framework import serializers

from marketplace.models import Bid_status, Post, Currency, Bid
from marketplace.serializers import UserSerializer, PostSerializer, CurrencySerializer
from marketplace.services import place_bid


class BidStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid_status
        fields = ['id', 'name', 'description', 'is_active']


def validate_post_id(value):
    """Valide que le post peut recevoir des enchères"""
    if not value.can_receive_bids():
        raise serializers.ValidationError("Ce post n'accepte pas d'enchères")
    return value


def validate_price(value):
    if value <= 0:
        raise serializers.ValidationError("Le prix doit être positif")
    return value


def get_is_highest(obj):
    return obj.post.get_highest_bid() == obj


def get_current_status(obj):
    status = obj.get_status_bid()
    return BidStatusSerializer(status).data if status else None


class BidSerializer(serializers.ModelSerializer):
    # Relations en lecture seule
    user = UserSerializer(read_only=True)
    post = PostSerializer(read_only=True)
    currency = CurrencySerializer(read_only=True)

    # Relations en écriture seule
    post_id = serializers.PrimaryKeyRelatedField(
        queryset=Post.objects.all(), source='post', write_only=True
    )
    currency_id = serializers.PrimaryKeyRelatedField(
        queryset=Currency.objects.all(), source='currency', write_only=True, required=False
    )

    # Champs calculés
    current_status = serializers.SerializerMethodField()
    is_highest = serializers.SerializerMethodField()

    class Meta:
        model = Bid
        fields = [
            'id', 'price', 'message', 'created_at', 'updated_at', 'is_active',

            # Relations (lecture)
            'user', 'post', 'currency',

            # Relations (écriture)
            'post_id', 'currency_id',

            # Champs calculés
            'current_status', 'is_highest'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'user']

    def validate(self, attrs):
        """Validation croisée"""
        post = attrs.get('post')
        user = self.context['request'].user

        # Vérifier que l'utilisateur n'enchérit pas sur son propre post
        if post and post.user == user:
            raise serializers.ValidationError("Vous ne pouvez pas enchérir sur votre propre post")

        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        post = validated_data['post']
        price = validated_data['price']

        # Utiliser la devise du post par défaut
        if 'currency' not in validated_data:
            validated_data['currency'] = post.currency

        # Utiliser le service pour créer l'enchère
        try:
            bid = place_bid(user, price, post.id)
            return bid
        except ValueError as e:
            raise serializers.ValidationError({'detail': str(e)})


def get_status_history(obj):
    """Retourne l'historique des statuts"""
    relations = obj.status_relations.select_related('status', 'changed_by').order_by('-date_changed')
    return [
        {
            'status': relation.status.name,
            'date_changed': relation.date_changed,
            'changed_by': relation.changed_by.username if relation.changed_by else None,
            'comment': relation.comment
        }
        for relation in relations
    ]


class BidDetailSerializer(BidSerializer):
    """Serializer détaillé pour les enchères avec informations complètes"""

    status_history = serializers.SerializerMethodField()

    class Meta(BidSerializer.Meta):
        fields = BidSerializer.Meta.fields + ['status_history']


    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Le prix doit être supérieur à zéro.")
        return value

class PlaceBidSerializer(serializers.Serializer):
    price = serializers.FloatField(min_value=0.01)
    message = serializers.CharField(required=False, allow_blank=True, max_length=500)

    def validate(self, data):
        user = self.context.get("request").user
        post = self.context.get("post")

        if not post:
            raise serializers.ValidationError("Le post est introuvable.")

        if post.user.id == user.id:
            raise serializers.ValidationError("Vous ne pouvez pas enchérir sur votre propre post.")

        current_status = post.get_status_post()
        if not current_status:
            raise serializers.ValidationError("Ce post n’a pas de statut actif.")

        if current_status.name.lower() not in ["published", "negociation", "publié", "en négociation"]:
            raise serializers.ValidationError(
                f"Ce post ne peut pas recevoir d'enchères car son statut est '{current_status.name}'."
            )

        return data

    def create(self, validated_data):
        user = self.context.get("request").user
        post = self.context.get("post")
        price = validated_data.get('price')
        message = validated_data.get('message', '')

        try:
            # place_bid doit accepter maintenant aussi le paramètre message
            bid = place_bid(user=user, bid_price=price, post_id=post.id, message=message)
            return bid
        except ValueError as e:
            raise serializers.ValidationError({'detail': str(e)})