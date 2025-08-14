from django.db import models

from marketplace.models import User


class Message_status(models.Model):
    status = models.CharField(max_length=50)
    expiration = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class Chat(models.Model):
    id_post = models.ForeignKey('marketplace.Post', on_delete=models.CASCADE)
    id_status = models.ForeignKey(Message_status, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class TypeMessage(models.Model):
    type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    message = models.TextField()
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    id_type_message = models.ForeignKey(TypeMessage, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
