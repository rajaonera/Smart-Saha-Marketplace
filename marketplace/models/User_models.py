from django.contrib.auth.models import AbstractUser
from django.db import models

class CategorieUser(models.Model):
    categorie = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.categorie

class User(AbstractUser):
    justificatif_url = models.URLField(blank=True, null=True)
    id_categorie_user = models.ForeignKey(CategorieUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.username
