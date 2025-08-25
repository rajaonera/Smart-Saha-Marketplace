from django.utils import timezone

from marketplace.models import Bid, Bid_status, BidStatusRelation, Message


def update_bid(bid: Bid, data: dict) -> Bid:
    """
    Met à jour une enchère si elle est encore au statut 'proposée'
    """
    if bid.get_status_bid().name.lower() != "proposée":
        raise ValueError("Seules les enchères au statut 'proposée' peuvent être modifiées.")

    # Mise à jour des champs autorisés
    price = data.get("price")
    message = data.get("message")

    if price is not None:
        if float(price) <= 0:
            raise ValueError("Le prix doit être supérieur à zéro.")
        bid.price = price

    if message is not None:
        bid.message = message

    bid.updated_at = timezone.now()
    bid.save()

    return bid


def cancel_bid(bid: Bid, user=None, comment="Annulation par l'utilisateur") -> Bid:
    """
    Annule une enchère : ajoute un statut 'annulée' dans l'historique
    """
    current_status = bid.get_status_bid()
    if current_status.name.lower() in ["acceptée", "annulée"]:
        raise ValueError(f"L'enchère ne peut pas être annulée car elle est déjà au statut '{current_status.name}'.")

    try:
        cancelled_status = Bid_status.objects.get(name__iexact="annulée")
    except Bid_status.DoesNotExist:
        raise ValueError("Le statut 'annulée' n'existe pas dans la base.")

    BidStatusRelation.objects.create(
        bid=bid,
        status=cancelled_status,
        changed_by=user,
        comment=comment
    )

    return bid


def accept_bid(bid: Bid, user=None, comment="Enchère acceptée") -> Bid:
    """
    Accepte une enchère : modifie son statut à 'acceptée'
    """
    current_status = bid.get_status_bid()
    if current_status.name.lower() != "proposée":
        raise ValueError("Seules les enchères proposées peuvent être acceptées.")

    try:
        accepted_status = Bid_status.objects.get(name__iexact="acceptée")
    except Bid_status.DoesNotExist:
        raise ValueError("Le statut 'acceptée' n'existe pas.")

    BidStatusRelation.objects.create(
        bid=bid,
        status=accepted_status,
        changed_by=user,
        comment=comment
    )

    return bid


def reject_bid(bid, owner, continue_negotiation: bool, message: str = ""):
    """
    Permet au propriétaire du post de refuser une enchère.
    - Si `continue_negotiation` est False → stoppe la négociation.
    - Si `continue_negotiation` est True → l'enchère reste active.
    - Un message peut être ajouté au fil de discussion.

    Args:
        bid (Bid): l'enchère à refuser
        owner (User): l'utilisateur propriétaire du post
        continue_negotiation (bool): si True, la négociation continue
        message (str): message optionnel à envoyer dans le chat

    Raises:
        ValueError: si l'utilisateur n'est pas propriétaire
    """

    if bid.post.user != owner:
        raise ValueError("Vous n'êtes pas autorisé à rejeter cette enchère.")

    # Statuts possibles
    refused_status = Bid_status.objects.get(name="refusée")
    stopped_status = Bid_status.objects.get(name="arrêtée")  # à créer si pas encore en DB

    # 1. Ajouter le nouveau statut
    status_to_apply = refused_status if continue_negotiation else stopped_status

    BidStatusRelation.objects.create(
        bid=bid,
        status=status_to_apply,
        changed_by=owner,
        comment="Refus manuel via API"
    )

    # 2. Ajouter un message au fil de discussion
    if message:
        Message.objects.create(
            post=bid.post,
            sender=owner,
            receiver=bid.user,
            bid=bid,
            content=message,
            timestamp=timezone.now()
        )

    return bid

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
