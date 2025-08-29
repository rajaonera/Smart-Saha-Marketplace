from django.db import models


class Category_Semence(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

class Semence(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category_Semence,related_name='category_to', on_delete=models.CASCADE)
    price = models.FloatField()
    quantity = models.FloatField()
    image = models.ImageField(upload_to='semences/')
    created_at = models.DateTimeField(auto_now_add=True, blank=False , null=False)
    updated_at = models.DateTimeField(auto_now=True , blank=False , null=False)
    user = models.ForeignKey('marketplace.User', on_delete=models.CASCADE)
    unit = models.ForeignKey('marketplace.Unit', on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=50)

    class Meta:
        unique_together = ('name', 'category')

    def __init__(self, name, price,category , quantity, image, user, unit):
        self.name = name
        self.category = category
        self.price = price
        self.quantity = quantity
        self.image = image
        self.user = user
        self.unit = unit

    def __str__(self):
        return f"{self.name} - {self.category} - {self.price} - {self.quantity} - {self.user} - {self.unit}"

    def __clean__(self):
        if self.quantity <= 0:
            raise ValueError("quantite invalie")
        if self.price <= 0:
            raise ValueError("prix invalide")
        if self.name == "" or self.category == "" or self.unit =="":
            raise ValueError("nom ou categorie ou unite invalide")
        if self.user  == "":
            raise ValueError("utilisateur invalide")

class Log_semence(models.Model):
    etat = models.CharField(max_length=255)
    quantity =  models.FloatField()
    user = models.ForeignKey('marketplace.User', on_delete=models.CASCADE , blank=True, null=True)
    semence = models.ForeignKey('Semence', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __init__(self, etat, quantity, user, semence):
        self.etat = etat
        self.semence = semence
        self.quantity = quantity
        self.user = user

    def __str__(self):
        return f"{self.etat} - {self.quantity} - {self.user}"

    def __clean__(self):
        if self.quantity <= 0:
            raise ValueError("quantite invalide")
        if self.type == "":
            raise ValueError("nom ou categorie ou unite invalide")
        if self.quantity == "":
            raise ValueError("quantite invalide")
        if  self.semence == "":
            raise ValueError("semence invalide")