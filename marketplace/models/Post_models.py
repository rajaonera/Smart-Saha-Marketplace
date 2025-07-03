from django.db import models

class TypePost(models.Model):
    type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

class CategoriePost(models.Model):
    categorie = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

class Currency(models.Model):
    currency = models.CharField(max_length=50)
    iso_code = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

class Unit(models.Model):
    unit = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)


class Label(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    product = models.CharField(max_length=50)
    id_unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Post_status(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Post(models.Model):
    id_type_post = models.ForeignKey(TypePost, on_delete=models.CASCADE)
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    id_user = models.ForeignKey('marketplace.User', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()
    location = models.CharField(max_length=255)
    image_url = models.URLField(max_length=255, blank=True, null=True)
    id_categorie_post = models.ForeignKey(CategoriePost, on_delete=models.CASCADE)
    id_currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    labels = models.ManyToManyField(Label, blank=True)
    status = models.ManyToManyField(Post_status, blank=False,through='PostStatusRelation')

    def __str__(self):
        return f"Détails pour {self.product.product}"

    def changer_statut(self, nouveau_statut: Post_status):
        if not isinstance(nouveau_statut, Post_status):
            raise ValueError("Statut invalide")

        PostStatusRelation.objects.create(post=self, status=nouveau_statut)
        
class PostStatusRelation(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    status = models.ForeignKey(Post_status, on_delete=models.CASCADE)
    date_changed = models.DateTimeField(auto_now_add=True)
