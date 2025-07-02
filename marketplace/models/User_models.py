from django.db import models

class CategorieUser(models.Model):
    categorie = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    justificatif_url = models.URLField(blank=True, null=True)
    id_categorie_user = models.ForeignKey(CategorieUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Password(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
