from marketplace.models import Chat, Post, Message

def get_chat_by_post(post: Post):
    return Chat.objects.filter(post=post)


def create_chat(chat: Chat, post : Post):
    finded_chat = get_chat_by_post(post)
    if finded_chat:
        raise Exception("Chat already exists")
    chat.save()

def create_message(chat: Chat, message : Message):
    if chat is None or message is None:
        raise Exception("Chat or Message are None")
