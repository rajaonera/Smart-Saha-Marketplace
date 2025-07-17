from typing import Any

from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


class TypePost(models.Model):
    type = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.type
    
    def validate(self, data):
        if 'id' in data:
            raise serializers.ValidationError({"id": "Le champ 'id' ne peut pas être modifié."})
        if 'created_at' in data:
            raise serializers.ValidationError({"created_at": "Le champ 'created_at' ne peut pas être modifié."})
        return data
        return self.type

    class Meta:
        verbose_name = "Type de post"
        verbose_name_plural = "Types de posts"


class CategoriePost(models.Model):
    categorie = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.categorie

    class Meta:
        verbose_name = "Catégorie de post"
        verbose_name_plural = "Catégories de posts"


class Currency(models.Model):
    currency = models.CharField(max_length=50)
    iso_code = models.CharField(max_length=3, unique=True)
    symbol = models.CharField(max_length=5, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.currency} ({self.iso_code})"

    class Meta:
        verbose_name = "Devise"
        verbose_name_plural = "Devises"


class Unit(models.Model):
    unit = models.CharField(max_length=50, unique=True)
    abbreviation = models.CharField(max_length=10, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.unit

    class Meta:
        verbose_name = "Unité"
        verbose_name_plural = "Unités"


class Label(models.Model):
    name = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=7, default="#000000")  # Couleur hex
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Label"
        verbose_name_plural = "Labels"


class Product(models.Model):
    product = models.CharField(max_length=50)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='products')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product} ({self.unit})"

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"

class Post_status(models.Model):
    name = models.CharField(max_length=255, unique=True, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}, {self.description}, {self.is_active}, {self.created_at} "

    class Meta:
        verbose_name = "Statut de post"
        verbose_name_plural = "Statuts de posts"

    def save(self, *args, **kwargs):
        self.name = str(self.name)
        self.description = str(self.description)


def get_allowed_transitions():
    return {
    "None": ["brouillon", "published"],  # Premier statut
    "brouillon": ["published", "supprimé"],
    "published": ["négociation", "vendu", "supprimé"],
    "négociation": ["vendu", "published", "supprimé"],
    "vendu": ["supprimé"],
    "supprimé": [],  # Pas de retour possible
}

def is_valid_status_transition(current_status, new_status: Post_status):
    if new_status is None:
        return False
    # Règles métier pour les transitions
    transitions = get_allowed_transitions()
    if current_status == "None":
        current = current_status
        print("current status: ", current)
        return new_status.name in transitions.get(current, set())

    else:
        current = current_status.name if current_status else None
        print("current status: ", current)
        return new_status.name in transitions.get(current, set())


class Post(models.Model):
    # Relations avec convention Django
    type_post = models.ForeignKey(TypePost, on_delete=models.CASCADE, related_name='posts')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='posts')
    user = models.ForeignKey('marketplace.User', on_delete=models.CASCADE, related_name='posts')
    categorie_post = models.ForeignKey(CategoriePost, on_delete=models.CASCADE, related_name='posts')
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='posts')

    # Champs principaux
    title = models.CharField(max_length=255)
    description = models.TextField()
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    location = models.CharField(max_length=255)
    image_url = models.URLField(max_length=500, blank=True, null=True)

    # Relations many-to-many
    labels = models.ManyToManyField(Label, blank=True, related_name='posts')
    status = models.ManyToManyField(Post_status, through='PostStatusRelation', related_name='posts', default=None)

    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id_user = None  # ok si champ custom temporaire
        # self.bids = None ← ✘ à retirer

    def __str__(self):
        return f"{self.title} - {self.product.product}"

    def clean(self):
        """Validation personnalisée"""
        if self.quantity <= 0:
            raise ValidationError("La quantité doit être positive")
        if self.price <= 0:
            raise ValidationError("Le prix doit être positif")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def changer_statut(self, nouveau_statut, utilisateur=None, commentaire=""):
        from marketplace.models import PostStatusRelation

        if isinstance(nouveau_statut, int):
            nouveau_statut = Post_status.objects.get(pk=nouveau_statut)

        statut_actuel = self.status_relations.order_by('-date_changed').first().status \
            if self.status_relations.exists() else "None"
        #
        # if not is_valid_status_transition(statut_actuel, nouveau_statut):
        #     print("is_valid_status_transition: ",  nouveau_statut)
        #     return False

        PostStatusRelation.objects.create(
            post=self,
            status=nouveau_statut,
            changed_by=utilisateur or self.user,
            comment=commentaire
        )
        return True

    def get_status_post(self):
        """
        Retourne le statut actuel du post
        """
        latest_relation = PostStatusRelation.objects.filter(post=self).order_by('-date_changed').first()
        return latest_relation.status if latest_relation else None

    def get_highest_bid(self):
        """
        Retourne l'enchère la plus élevée pour ce post
        """
        return self.bids.order_by('-price').first()

    def get_active_bids(self):
        """
        Retourne les enchères actives (statut 'proposée')
        """
        return self.bids.filter(
            status_relations__status__name="proposée"
        ).distinct()

    def get_accepted_bid(self):
        """
        Retourne l'enchère acceptée s'il y en a une
        """
        return self.bids.filter(
            status_relations__status__name="acceptée"
        ).first()

    def has_active_bids(self):
        """
        Vérifie s'il y a des enchères actives
        """
        return self.get_active_bids().exists()

    def can_receive_bids(self):
        """
        Vérifie si le post peut recevoir des enchères
        """
        current_status = self.get_status_post()
        if not current_status:
            return False
        return current_status.name.lower() in ["published", "négociation"]

    def get_total_bids(self):
        return self.bids.count()

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['type_post', 'categorie_post']),
            models.Index(fields=['price']),
        ]


class PostStatusRelation(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='status_relations')
    status = models.ForeignKey(Post_status, on_delete=models.CASCADE, related_name='post_relations')
    date_changed = models.DateTimeField(auto_now_add=True)
    changed_by = models.ForeignKey('marketplace.User', on_delete=models.SET_NULL, null=True, blank=True)
    comment = models.TextField(blank=True)


    class Meta:
        verbose_name = "Relation statut post"
        verbose_name_plural = "Relations statuts posts"
        ordering = ['-date_changed']
        unique_together = ['post', 'status', 'date_changed']

