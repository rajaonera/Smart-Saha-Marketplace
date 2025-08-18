from datetime import date

from marketplace.models import Message, Chat, Bid, User


def envoi_message(bid, sender, receiver , message: str = "", ):
  try:
    message  = Message(sender=sender, receiver=receiver, message=message)
    message.created_at(date.datetime.now())
    message.save()

  except Exception as e:
   raise ValueError("message non envoye")

def chat_message(bid : int, sender : User , message: str = "", ):
  try:
    bid_object = Bid.objects.get(id=bid)
    chat = Chat.objects.get(id_post = bid_object.post.id)

    if chat is None:
      chat = Chat.objects.create(
        id_post=bid_object.post.id,
        id_status =
      )
  except Exception as e:
    raise ValueError("chat non trouve ou non cree ")


# def changer_statut_post(post_id: int, statut_id: int, changed_by: User = None, comment: str = ""):
#     try:
#         post = Post.objects.get(id=post_id)
#         statut = Post_status.objects.get(id=statut_id)
#     except (Post.DoesNotExist, Post_status.DoesNotExist):
#         raise ValueError("Post ou statut introuvable")
#
#     current_status = post.get_status_post()
#     if not _is_valid_status_transition(current_status, statut):
#         raise ValueError(f"Transition invalide de {current_status} vers {statut}")
#
#     PostStatusRelation.objects.create(
#         post=post,
#         status=statut,
#         changed_by=changed_by,
#         comment=comment
#     )
#
#     return post

