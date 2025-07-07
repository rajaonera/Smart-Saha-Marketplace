from rest_framework import serializers
from marketplace.models import (
    TypePost, CategoriePost, Currency, Unit, Product, Post, Post_status,
    Label,
)
from marketplace.serializers import UserSerializer
from marketplace.serializers.Bid_serialisers import BidSerializer

class TypePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypePost
        fields = ['id', 'type', 'created_at']


class CategoriePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriePost
        fields = ['id', 'categorie', 'created_at']


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['id', 'currency', 'iso_code', 'symbol', 'created_at']


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ['id', 'unit', 'abbreviation', 'created_at']


class ProductSerializer(serializers.ModelSerializer):
    unit = UnitSerializer(read_only=True)
    unit_id = serializers.PrimaryKeyRelatedField(
        queryset=Unit.objects.all(), source='unit', write_only=True
    )

    class Meta:
        model = Product
        fields = ['id', 'product', 'description', 'unit', 'unit_id', 'created_at']


class PostStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post_status
        fields = ['id', 'name', 'description', 'is_active']


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['id', 'name', 'color', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    # Relations en lecture seule (avec détails)
    type_post = TypePostSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    categorie_post = CategoriePostSerializer(read_only=True)
    currency = CurrencySerializer(read_only=True)
    labels = LabelSerializer(many=True, read_only=True)

    # Relations en écriture seule (IDs)
    type_post_id = serializers.PrimaryKeyRelatedField(
        queryset=TypePost.objects.all(), source='type_post', write_only=True
    )
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )
    categorie_post_id = serializers.PrimaryKeyRelatedField(
        queryset=CategoriePost.objects.all(), source='categorie_post', write_only=True
    )
    currency_id = serializers.PrimaryKeyRelatedField(
        queryset=Currency.objects.all(), source='currency', write_only=True
    )
    labels_ids = serializers.PrimaryKeyRelatedField(
        queryset=Label.objects.all(), many=True, source='labels', write_only=True, required=False
    )

    # Champs calculés
    current_status = serializers.SerializerMethodField()
    total_bids = serializers.SerializerMethodField()
    highest_bid = serializers.SerializerMethodField()
    can_receive_bids = serializers.SerializerMethodField()

    # Statut pour la création
    initial_status_id = serializers.PrimaryKeyRelatedField(
        queryset=Post_status.objects.filter(is_active=True),
        write_only=True,
        required=False
    )

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'description', 'quantity', 'price', 'location',
            'image_url', 'created_at', 'updated_at', 'is_active',

            # Relations (lecture)
            'type_post', 'product', 'user', 'categorie_post', 'currency', 'labels',

            # Relations (écriture)
            'type_post_id', 'product_id', 'categorie_post_id', 'currency_id', 'labels_ids',

            # Champs calculés
            'current_status', 'total_bids', 'highest_bid', 'can_receive_bids',

            # Statut initial
            'initial_status_id'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'user']

    def create(self, validated_data):
        labels = validated_data.pop('labels', [])
        initial_status_id = validated_data.pop('initial_status_id', None)

        # Assigner l'utilisateur connecté
        validated_data['user'] = self.context['request'].user

        # Créer le post
        post = Post.objects.create(**validated_data)

        # Assigner les labels
        if labels:
            post.labels.set(labels)

        # Assigner le statut initial
        if initial_status_id:
            post.changer_statut(initial_status_id)
        else:
            # Statut par défaut
            try:
                default_status = Post_status.objects.get(name="brouillon")
                post.changer_statut(default_status)
            except Post_status.DoesNotExist:
                pass  # Pas de statut par défaut

        return post

    def update(self, instance, validated_data):
        labels = validated_data.pop('labels', None)
        validated_data.pop('initial_status_id', None)  # Ignore pour les mises à jour

        # Mettre à jour les champs
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Mettre à jour les labels
        if labels is not None:
            instance.labels.set(labels)

        instance.save()
        return instance


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


class PostDetailSerializer(PostSerializer):
    """Serializer détaillé pour les posts avec informations complètes"""

    status_history = serializers.SerializerMethodField()
    active_bids = serializers.SerializerMethodField()
    accepted_bid = serializers.SerializerMethodField()

    class Meta(PostSerializer.Meta):
        fields = PostSerializer.Meta.fields + ['status_history', 'active_bids', 'accepted_bid']

    def get_active_bids(self, obj):
        """Retourne les enchères actives"""
        active_bids = obj.get_active_bids()
        return BidSerializer(active_bids, many=True, context=self.context).data

    def get_accepted_bid(self, obj):
        """Retourne l'enchère acceptée"""
        accepted_bid = obj.get_accepted_bid()
        return BidSerializer(accepted_bid, context=self.context).data if accepted_bid else None

#
# def get_current_status(obj):
#     status = obj.get_status_post()
#     return status.name if status else None
#
#
# def get_total_bids(obj):
#     return obj.bids.count()

    def validate_image_url(value):
        if value and not value.startswith('https://'):
            raise serializers.ValidationError("L'URL doit commencer par ou https://")
        return value

    def validate_quantity(value):
        if value <= 0:
            raise serializers.ValidationError("La quantité doit être positive")
        return value

    def validate_price(value):
        if value <= 0:
            raise serializers.ValidationError("Le prix doit être positif")
        return value

    def get_can_receive_bids(obj):
        return obj.can_receive_bids()

    def get_highest_bid(obj):
        highest_bid = obj.get_highest_bid()
        if highest_bid:
            return {
                'id': highest_bid.id,
                'price': highest_bid.price,
                'currency': highest_bid.currency.iso_code,
                'created_at': highest_bid.created_at
            }
        return None

    def get_total_bids(obj):
        return obj.bids.count()

    def get_current_status(obj):
        status = obj.get_status_post()
        return PostStatusSerializer(status).data if status else None


def get_highest_bid_price(obj):
    highest_bid = obj.get_highest_bid()
    return highest_bid.price if highest_bid else None


class PostSummarySerializer(serializers.ModelSerializer):
    """Serializer léger pour les listes de posts"""

    current_status = serializers.SerializerMethodField()
    total_bids = serializers.SerializerMethodField()
    highest_bid_price = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'price', 'location', 'image_url', 'created_at',
            'current_status', 'total_bids', 'highest_bid_price'
        ]

