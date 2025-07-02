from rest_framework import serializers
from marketplace.models import (
    TypePost, CategoriePost, Currency, Unit, Product, Post
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


class PostSerializer(serializers.ModelSerializer):
    id_type_post = TypePostSerializer(read_only=True)
    id_type_post_id = serializers.PrimaryKeyRelatedField(
        queryset=TypePost.objects.all(), source='id_type_post', write_only=True
    )

    id_product = ProductSerializer(read_only=True)
    id_product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='id_product', write_only=True
    )

    id_user = serializers.IntegerField(read_only=True)  # à définir via JWT
    id_categorie_post = CategoriePostSerializer(read_only=True)
    id_categorie_post_id = serializers.PrimaryKeyRelatedField(
        queryset=CategoriePost.objects.all(), source='id_categorie_post', write_only=True
    )

    id_currency = CurrencySerializer(read_only=True)
    id_currency_id = serializers.PrimaryKeyRelatedField(
        queryset=Currency.objects.all(), source='id_currency', write_only=True
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
        ]
