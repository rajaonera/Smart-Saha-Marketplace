from rest_framework import serializers
from marketplace.models import Message_status, Chat, TypeMessage, Message, Post, User


class MessageStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message_status
        fields = ['id', 'status', 'expiration', 'created_at']


class ChatSerializer(serializers.ModelSerializer):
    id_post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    id_status = MessageStatusSerializer(read_only=True)
    id_status_id = serializers.PrimaryKeyRelatedField(
        queryset=Message_status.objects.all(), source='id_status', write_only=True
    )

    class Meta:
        model = Chat
        fields = [
            'id',
            'id_post',
            'id_status',
            'id_status_id',
            'created_at',
        ]


class TypeMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeMessage
        fields = ['id', 'type', 'created_at']


class MessageSerializer(serializers.ModelSerializer):
    id_user = serializers.PrimaryKeyRelatedField(read_only=True)  # injecté via JWT
    id_chat = serializers.PrimaryKeyRelatedField(queryset=Chat.objects.all())
    id_type_message = TypeMessageSerializer(read_only=True)
    id_type_message_id = serializers.PrimaryKeyRelatedField(
        queryset=TypeMessage.objects.all(), source='id_type_message', write_only=True
    )

    class Meta:
        model = Message
        fields = [
            'id',
            'message',
            'id_user',
            'id_chat',
            'id_type_message',
            'id_type_message_id',
            'created_at',
        ]
