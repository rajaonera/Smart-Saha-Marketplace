from django.utils import timezone
from marketplace.models import Bid, Bid_status, BidStatusRelation


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


def reject_bid(bid: Bid, user=None, comment="Enchère refusée") -> Bid:
    """
    Refuse une enchère : modifie son statut à 'refusée'
    """
    current_status = bid.get_status_bid()
    if current_status.name.lower() != "proposée":
        raise ValueError("Seules les enchères proposées peuvent être refusées.")

    try:
        rejected_status = Bid_status.objects.get(name__iexact="refusée")
    except Bid_status.DoesNotExist:
        raise ValueError("Le statut 'refusée' n'existe pas.")

    BidStatusRelation.objects.create(
        bid=bid,
        status=rejected_status,
        changed_by=user,
        comment=comment
    )

    return bid
