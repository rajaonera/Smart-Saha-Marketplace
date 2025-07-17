from rest_framework import serializers
from marketplace.models import Bid_status, Post, Currency, Bid

class BidStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid_status
        fields = ['id', 'name', 'description', 'is_active']


class BidSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    post = serializers.SerializerMethodField()
    currency = serializers.SerializerMethodField()
    current_status = serializers.SerializerMethodField()
    is_highest = serializers.SerializerMethodField()

    post_id = serializers.PrimaryKeyRelatedField(
        queryset=Post.objects.all(), source='post', write_only=True
    )
    currency_id = serializers.PrimaryKeyRelatedField(
        queryset=Currency.objects.all(), source='currency', write_only=True, required=False
    )

    class Meta:
        model = Bid
        fields = [
            'id', 'price', 'message', 'created_at', 'updated_at', 'is_active',
            'user', 'post', 'currency',
            'post_id', 'currency_id',
            'current_status', 'is_highest'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'user']

    def get_user(self, obj):
        from marketplace.serializers.User_serializers import UserSerializer
        return UserSerializer(obj.user).data

    def get_post(self, obj):
        from marketplace.serializers.Post_serializers import PostSerializer
        return PostSerializer(obj.post).data

    def get_currency(self, obj):
        from  marketplace.serializers.Post_serializers import CurrencySerializer
        return CurrencySerializer(obj.currency).data

    def get_current_status(self, obj):
        status = obj.get_status_bid()
        return BidStatusSerializer(status).data if status else None

    def get_is_highest(self, obj):
        return obj.post.get_highest_bid() == obj

    def validate(self, attrs):
        post = attrs.get('post')
        user = self.context['request'].user
        if post and post.user == user:
            raise serializers.ValidationError("Vous ne pouvez pas enchérir sur votre propre post.")
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        post = validated_data['post']
        price = validated_data['price']
        if 'currency' not in validated_data:
            validated_data['currency'] = post.currency
        try:
            from marketplace.services.Post_service import place_bid
            bid = place_bid(user, price, post.id)
            return bid
        except ValueError as e:
            raise serializers.ValidationError({'detail': str(e)})

class BidDetailSerializer(BidSerializer):
    status_history = serializers.SerializerMethodField()

    class Meta(BidSerializer.Meta):
        fields = BidSerializer.Meta.fields + ['status_history']

    def get_status_history(self, obj):
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
            from marketplace.services.Post_service import place_bid
            bid = place_bid(user=user, bid_price=price, post_id=post.id, message=message)
            return bid
        except ValueError as e:
            raise serializers.ValidationError({'detail': str(e)})

class RejectBidSerializer(serializers.Serializer):
    continue_negotiation = serializers.BooleanField()
    message = serializers.CharField(required=False, allow_blank=True, max_length=1000)

    def validate(self, data):
        if not data['continue_negotiation'] and not data.get('message'):
            raise serializers.ValidationError("Un message est requis si vous arrêtez la négociation.")
        return data
