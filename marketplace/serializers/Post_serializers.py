from rest_framework import serializers

from marketplace.models import (
    TypePost, CategoriePost, Currency, Unit, Product, Post, Post_status,
    Label, Category_Semence, User, Semence,
)

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
        read_only_fields = ['id', 'created_at']

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

def validate_name(value):
    if not value.isalpha():
        raise serializers.ValidationError("Le champ 'name' doit contenir uniquement des caractères alphabétiques.")
    return value

class PostStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post_status
        fields = ['id', 'name', 'description','is_active','created_at']

        extra_kwargs = {
            'name': {'error_messages': {'unique': "Ce nom de statut existe déjà."}},
            'description': {'required': False}
        }

    def validate(self, data):
        if 'name' not in data or not data['name']:
            raise serializers.ValidationError({"name": "Le champ 'name' est requis."})
        return data


    # def create(self, validated_data):    
    #     print("Données validées reçues :", validated_data)  # Debugging
    #     instance = Post_status.objects.create(**validated_data)
    #     print("Instance créée :", instance)  # Debugging
    #     return instance

class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['id', 'name', 'color', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    # Relations en lecture seule (avec détails)
    from  marketplace.serializers.User_serializers import UserSerializer

    user = UserSerializer(read_only=True)
    type_post = TypePostSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
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
        initial_status_id = validated_data.pop('initial_status_id', id)

        # Assigner l'utilisateur connecté
        validated_data['user'] = self.context['request'].user

        # Créer le post
        post = Post.objects.create(**validated_data)

        # Assigner les labels
        if labels:
            post.labels.set(labels)

        if initial_status_id:
            post.status.set(initial_status_id)

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


    def get_current_status(self, instance):
        return instance.get_status_post()

    def get_total_bids(self, instance):
        return instance.get_total_bids()

    def get_highest_bid(self, instance):
        return instance.get_highest_bid()

    def get_can_receive_bids(self , obj : Post):
        return obj.can_receive_bids()

    def get_highest_bid_price(self, instance):
        return instance.get_highest_bid().price

class PostDetailSerializer(PostSerializer):
    """Serializer détaillé pour les posts avec informations complètes"""


    status_history = serializers.SerializerMethodField()
    active_bids = serializers.SerializerMethodField()
    accepted_bid = serializers.SerializerMethodField()

    class Meta(PostSerializer.Meta):
        fields = PostSerializer.Meta.fields + ['status_history', 'active_bids', 'accepted_bid']

    def get_active_bids(self, obj):
        """Retourne les enchères actives"""
        from marketplace.serializers.Bid_serialisers import BidSerializer
        active_bids = obj.get_active_bids()
        return BidSerializer(active_bids, many=True, context=self.context).data

    def get_accepted_bid(self, obj):
        """Retourne l'enchère acceptée"""
        accepted_bid = obj.get_accepted_bid()
        from marketplace.serializers.Bid_serialisers import BidSerializer
        return BidSerializer(accepted_bid, context=self.context).data if accepted_bid else None

    def get_current_status(self , obj: Post):
        status = obj.get_status_post()
        return status.name if status else None


    def get_total_bids(self, obj : Post):
        return obj.bids.count()

    def validate_image_url(value : str):
        if value and not value.startswith('https://'):
            raise serializers.ValidationError("L'URL doit commencer par ou https://")
        return value

    def validate_quantity(value : float):
        if value <= 0:
            raise serializers.ValidationError("La quantité doit être positive")
        return value

    def validate_price(value : float):
        if value <= 0:
            raise serializers.ValidationError("Le prix doit être positif")
        return value

    def get_can_receive_bids(self , obj : Post):
        return obj.can_receive_bids()

    def get_highest_bid(self, obj : Post):
        highest_bid = obj.get_highest_bid()
        if highest_bid:
            return {
                'id': highest_bid.id,
                'price': highest_bid.price,
                'currency': highest_bid.currency.iso_code,
                'created_at': highest_bid.created_at
            }
        return None

    def get_highest_bid_price(self ,obj: Post):
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

class Category_SemenceSerializers(serializers.ModelSerializer):
    class meta:
        model = Category_Semence
        fields = ['id',
                  'categorie',
                  'created_at',
                  'updated_at']

class SemenceSerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category_Semence.objects.all(),
        source = 'category',
        write_only = True
    )
    category = Category_SemenceSerializers(read_only=True)

    unit_id = serializers.PrimaryKeyRelatedField(
        queryset=Unit.objects.all(),
        source='unit',
        write_only=True
    )
    unit = UnitSerializer(read_only=True)

    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user',
    )

    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class meta:
        fields = ['id',
                  'name',
                  'quantity',
                  'status',
                  'image',
                  'description',
                  'price' ,
                  'unit_id',
                  'unit',
                  'user_id',
                  'user',
                  'category_id',
                  'category',
                  'created_at',
                  'updated_at'
                  ]
        model = Semence
