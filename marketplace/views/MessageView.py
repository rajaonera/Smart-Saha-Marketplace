from rest_framework import permissions
from rest_framework import viewsets

from marketplace.models import (
    Chat, Message, TypeMessage, Message_status
)
from marketplace.serializers import (
    ChatSerializer,
    MessageSerializer,
    TypeMessageSerializer,
    MessageStatusSerializer,
)


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        return {'request': self.request}

class TypeMessageViewSet(viewsets.ModelViewSet):
    queryset = TypeMessage.objects.all()
    serializer_class = TypeMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

class MessageStatusViewSet(viewsets.ModelViewSet):
    queryset = Message_status.objects.all()
    serializer_class = MessageStatusSerializer
    permission_classes = [permissions.IsAuthenticated]