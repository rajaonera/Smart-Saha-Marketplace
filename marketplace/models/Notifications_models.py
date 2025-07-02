from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

class PostTag(models.Model):
    id_post = models.ForeignKey('marketplace.Post', on_delete=models.CASCADE)
    id_tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('id_post', 'id_tag')

class Notification(models.Model):
    id_user = models.ForeignKey('marketplace.User', on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    notification_type = models.CharField(max_length=50)
    reference_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)