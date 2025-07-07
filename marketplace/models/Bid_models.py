from typing import Any

from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

from marketplace.models import Post, Currency


# Modèles pour les enchères
class Bid_status(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Statut d'enchère"
        verbose_name_plural = "Statuts d'enchères"


class Bid(models.Model):
    user = models.ForeignKey('marketplace.User', on_delete=models.CASCADE, related_name='bids')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='bids')
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='bids')
    message = models.TextField(blank=True)

    # Relations
    status = models.ManyToManyField(Bid_status, through='BidStatusRelation', related_name='bids')

    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(args, kwargs)
        self.id = None

    def __str__(self):
        return f"Enchère {self.price} {self.currency.iso_code} sur {self.post.title}"

    def clean(self):
        highest_bid = self.post.get_highest_bid()
        if highest_bid and self.price <= highest_bid.price:
            raise ValidationError("Votre enchère doit dépasser l'enchère actuelle la plus élevée")
        if self.price <= 0:
            raise ValidationError("Le prix doit être positif")
        if self.user == self.post.user:
            raise ValidationError("Vous ne pouvez pas enchérir sur votre propre post")
        if not self.post.is_active:
            raise ValidationError("Vous ne pouvez pas enchérir sur un post inactif")

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            initial_status = Bid_status.objects.get(name="proposée")
            self.changer_statut(initial_status)

    def changer_statut(self, nouveau_statut, changed_by=None, comment=""):
        if not isinstance(nouveau_statut, Bid_status):
            raise ValueError("Statut invalide")

        BidStatusRelation.objects.create(
            bid=self,
            status=nouveau_statut,
            changed_by=changed_by,
            comment=comment
        )

    def get_status_bid(self):
        """
        Retourne le statut actuel de l'enchère
        """
        latest_relation = BidStatusRelation.objects.filter(bid=self).order_by('-date_changed').first()
        return latest_relation.status if latest_relation else None

    class Meta:
        verbose_name = "Enchère"
        verbose_name_plural = "Enchères"
        ordering = ['-created_at']
        unique_together = ['user', 'post', 'price']  # Éviter les doublons


class BidStatusRelation(models.Model):
    bid = models.ForeignKey(Bid, on_delete=models.CASCADE, related_name='status_relations')
    status = models.ForeignKey(Bid_status, on_delete=models.CASCADE, related_name='bid_relations')
    date_changed = models.DateTimeField(auto_now_add=True)
    changed_by = models.ForeignKey('marketplace.User', on_delete=models.SET_NULL, null=True, blank=True)
    comment = models.TextField(blank=True)

    class Meta:
        verbose_name = "Relation statut enchère"
        verbose_name_plural = "Relations statuts enchères"
        ordering = ['-date_changed']