from marketplace.models import Post, Post_status

def changer_statut_post(post_id: int, statut_id: int):
    post = Post.objects.get(id=post_id)
    statut = Post_status.objects.get(id=statut_id)

    post.changer_statut(statut)
    return post
