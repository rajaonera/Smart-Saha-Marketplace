from rest_framework import serializers
from marketplace.models import (
    TypePost, CategoriePost, Currency, Unit, Product, Post, Post_status, Label
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
        fields = ['id', 'currency', 'iso_code', 'created_at']


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ['id', 'unit', 'created_at']


class ProductSerializer(serializers.ModelSerializer):
    id_unit = UnitSerializer(read_only=True)
    id_unit_id = serializers.PrimaryKeyRelatedField(
        queryset=Unit.objects.all(), source='id_unit', write_only=True
    )

    class Meta:
        model = Product
        fields = ['id', 'product', 'id_unit', 'id_unit_id', 'created_at']


class PostStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post_status
        fields = ['id', 'name']


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['id', 'name']

class PostSerializer(serializers.ModelSerializer):
    id_type_post = TypePostSerializer(read_only=True)
    id_type_post_id = serializers.PrimaryKeyRelatedField(
        queryset=TypePost.objects.all(), source='id_type_post', write_only=True
    )

    id_product = ProductSerializer(read_only=True)
    id_product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='id_product', write_only=True
    )

    id_user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    id_categorie_post = CategoriePostSerializer(read_only=True)
    id_categorie_post_id = serializers.PrimaryKeyRelatedField(
        queryset=CategoriePost.objects.all(), source='id_categorie_post', write_only=True
    )

    id_currency = CurrencySerializer(read_only=True)
    id_currency_id = serializers.PrimaryKeyRelatedField(
        queryset=Currency.objects.all(), source='id_currency', write_only=True
    )

    # ✅ Labels (ManyToMany)
    labels = LabelSerializer(many=True, read_only=True)
    labels_ids = serializers.PrimaryKeyRelatedField(
        queryset=Label.objects.all(), many=True, write_only=True, source='labels', required=False
    )

    # ✅ Statuses (ManyToMany)
    status = PostStatusSerializer(many=True, read_only=True)
    status_ids = serializers.PrimaryKeyRelatedField(
        queryset=Post_status.objects.all(), many=True, write_only=True, source='status', required=False
    )

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'description',
            'quantity',
            'price',
            'location',
            'image_url',
            'created_at',

            'id_user',

            'id_type_post', 'id_type_post_id',
            'id_product', 'id_product_id',
            'id_categorie_post', 'id_categorie_post_id',
            'id_currency', 'id_currency_id',

            'labels', 'labels_ids',
            'status', 'status_ids',
        ]

    def create(self, validated_data):
        labels = validated_data.pop('labels', [])
        status = validated_data.pop('status', [])

        post = Post.objects.create(**validated_data)
        post.labels.set(labels)
        post.status.set(status)

        return post

    def update(self, instance, validated_data):
        labels = validated_data.pop('labels', None)
        status = validated_data.pop('status', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if labels is not None:
            instance.labels.set(labels)
        if status is not None:
            instance.statuses.set(status)

        instance.save()
        return instance
