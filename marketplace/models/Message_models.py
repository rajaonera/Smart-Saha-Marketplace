from django.db import models

# from marketplace.models import User


class Message_status(models.Model):
    status = models.CharField(max_length=50)
    expiration = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __init__(self, status, expiration):
        self.status = status
        self.expiration = expiration

    def __str__(self):
        return self.status

class Chat(models.Model):
    id_post = models.ForeignKey('marketplace.Post', on_delete=models.CASCADE)
    id_status = models.ForeignKey(Message_status, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __init__(self, id_post, id_status):
        self.id_post = id_post
        self.id_status = id_status

    def __str__(self):
        return f"{self.id_post.user.username} - {self.id_status.status}"

class TypeMessage(models.Model):
    type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __init__(self, type):
        self.type = type

    def __str__(self):
        return self.type

class Message(models.Model):
    message = models.TextField()
    id_user = models.ForeignKey('marketplace.User', on_delete=models.CASCADE)
    id_chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    id_type_message = models.ForeignKey(TypeMessage, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    def __init__(self, id_post, id_message , id_user , id_chat , id_type_message ):
        self.id_post = id_post
        self.id_message = id_message
        self.id_user = id_user
        self.id_chat = id_chat
        self.id_type_message = id_type_message
        from datetime import datetime
        self.created_at = datetime.now(),

    def __str__(self):
        return f"{self.id_post} {self.id_message} {self.id_chat} {self.id_type_message}"


