from django.db import models
from django.core.exceptions import ValidationError


class Review(models.Model):
    id_user_from = models.ForeignKey('marketplace.User', related_name='review_from', on_delete=models.CASCADE)
    id_user_to = models.ForeignKey('marketplace.User', related_name='review_to', on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Favorite(models.Model):
    id_user = models.ForeignKey('marketplace.User', on_delete=models.CASCADE)
    id_post = models.ForeignKey('marketplace.Post', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('id_user', 'id_post')

class Report(models.Model):
    id_user = models.ForeignKey('marketplace.User', on_delete=models.CASCADE)
    id_post = models.ForeignKey('marketplace.Post', on_delete=models.SET_NULL, blank=True, null=True)
    id_message = models.ForeignKey('marketplace.Message', on_delete=models.SET_NULL, blank=True, null=True)
    reason = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if (self.id_post and self.id_message) or (not self.id_post and not self.id_message):
            raise ValidationError('Un seul champ entre id_post ou id_message doit être renseigné.')

