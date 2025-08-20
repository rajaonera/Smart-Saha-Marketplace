from django.db import transaction

from marketplace.models import Post, Post_status, Bid, User, PostStatusRelation, Bid_status, BidStatusRelation


def changer_statut_post(post_id: int, statut_id: int, changed_by: User = None, comment: str = ""):
    try:
        post = Post.objects.get(id=post_id)
        statut = Post_status.objects.get(id=statut_id)
    except (Post.DoesNotExist, Post_status.DoesNotExist):
        raise ValueError("Post ou statut introuvable")

    current_status = post.get_status_post()
    if not _is_valid_status_transition(current_status, statut):
        raise ValueError(f"Transition invalide de {current_status} vers {statut}")

    PostStatusRelation.objects.create(
        post=post,
        status=statut,
        changed_by=changed_by,
        comment=comment
    )

    return post

def changer_statut(self, nouveau_statut: Bid_status):
    if not isinstance(nouveau_statut, Bid_status):
        raise ValueError("Statut d'enchère invalide")
    BidStatusRelation.objects.create(bid=self, status=nouveau_statut)

def _is_valid_status_transition(current_status, new_status):
    """
    Valide les transitions de statut autorisées
    """
    # Définir tes règles métier ici
    valid_transitions = {
        "brouillon": ["published", "supprimé"],
        "published": ["négociation", "vendu", "supprimé"],
        "négociation": ["vendu", "published", "supprimé"],
        "vendu": ["supprimé"],
    }

    if not current_status:
        return True  # Premier statut

    current_name = current_status.name.lower()
    new_name = new_status.name.lower()

    return new_name in valid_transitions.get(current_name, [])

def get_all_posts():
    return Post.objects.all()

def get_all_posts_by_user(user_id: int):
    return Post.objects.filter(id_user=user_id)

def get_post_by_id(post_id: int):
    return Post.objects.get(id=post_id)

def get_all_posts_by_status(status_id: int):
    return Post.objects.filter(status=status_id)


def place_bid(user: User, bid_price: float, post_id: int, message: str = ""):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        raise ValueError("Post introuvable")

    if post.user == user:
        raise ValueError("Vous ne pouvez pas enchérir sur votre propre post")

    if bid_price <= 0:
        raise ValueError("Le prix doit être positif")

    current_status = post.get_status_post()
    if not current_status or current_status.name.lower() not in ["published", "negociation"]:
        raise ValueError("Ce post n'accepte pas d'enchères")

    with transaction.atomic():
        new_bid = Bid.objects.create(
            user=user,
            post=post,
            price=bid_price,
            message=message,
            currency=post.currency  # par défaut la devise du post
        )

        initial_status = Bid_status.objects.get(name="proposée")
        new_bid.changer_statut(initial_status)

    return new_bid

def get_posts_with_filters(user_id=None, status_name=None, category_id=None):
    """
    Récupère les posts avec filtres optionnels
    """
    queryset = Post.objects.select_related(
        'id_user', 'id_product', 'id_type_post', 'id_currency'
    ).prefetch_related('labels', 'status')

    if user_id:
        queryset = queryset.filter(id_user=user_id)

    if status_name:
        queryset = queryset.filter(status__name=status_name)

    if category_id:
        queryset = queryset.filter(id_categorie_post=category_id)

    return queryset


def get_user_posts_summary(user_id: int):
    """
    Résumé des posts d'un utilisateur
    """
    posts = Post.objects.filter(id_user=user_id)

    return {
        'total_posts': posts.count(),
        'published_posts': posts.filter(status__name="published").count(),
        'sold_posts': posts.filter(status__name="vendu").count(),
        'draft_posts': posts.filter(status__name="brouillon").count(),
    }
