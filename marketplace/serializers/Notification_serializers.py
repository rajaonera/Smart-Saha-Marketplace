from rest_framework import serializers
from marketplace.models import Notification, User


class NotificationSerializer(serializers.ModelSerializer):
    id_user = serializers.PrimaryKeyRelatedField(read_only=True)  # injecté via JWT

    class Meta:
        model = Notification
        fields = [
            'id',
            'id_user',
            'message',
            'is_read',
            'notification_type',
            'reference_id',
            'created_at',
        ]
        read_only_fields = ['created_at']
