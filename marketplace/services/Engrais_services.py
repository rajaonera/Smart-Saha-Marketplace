from marketplace.models import Category_Semence, Semence

def get_all_semence():
    return Category_Semence.objects.all()

def get_semence_by_id(semence_id: int):
    return Category_Semence.objects.get(id=semence_id)

def get_all_semence_by_category(category_id: int):
    return Semence.objects.filter(id_category_semence=category_id)

def get_semence_by_name(name: str):
    return Semence.objects.get(name=name)

def get_semence_by_category_name(category_name: str):
    return Category_Semence.objects.get(name=category_name)

def get_semence_by_user(user_id: int):
    return Semence.objects.filter(id_user=user_id)

def create_semence(name: str, category_id: int, price: float, quantity: int, image: str, user_id: int , unit: int):
    from datetime import datetime
    return Semence.objects.create(name=name, category_id=category_id, price=price, quantity=quantity, image=image, user_id=user_id, unit=unit, updated_at=datetime.now())

def delete_semence(semence_id: int):
    return Semence.objects.get(id=semence_id).delete()

def update_semence(semence_id: int, name: str, category_id: int, price: float, quantity: int, image: str, user_id: int , unit: int):
    return Semence.objects.filter(id=semence_id).update(name=name, category_id=category_id, price=price, quantity=quantity, image=image, user_id=user_id, unit=unit)

def get_by_pice(min_price: float , max_price: float):
    return Semence.objects.filter(price__gte=min_price, price__lte=max_price)

def buy_semence(user_id: int, semence_id: int, quantity: int):
    semence =  get_semence_by_id(semence_id)
    from marketplace.models import User
    user = User.objects.get(id=user_id)
    if user is None:
        raise ValueError("user introuvable")
    if semence.quantity <= quantity:
        raise ValueError("quantite insuffisante")
    from datetime import datetime
    semence.update(quantity=quantity-quantity, updated_at=datetime.now())
    from marketplace.models import Log_semence
    log_semence = Log_semence.objects.get(
        semence = semence_id,
        etat = 'achat',
        quantity = semence.quantity,
        updated_at = datetime.now(),
        created_at = datetime.now(),
        user = user_id
    )
    log_semence.save()

def get_category_semence(category_id: int):
    return Category_Semence.objects.get(id=category_id)

def get_category_semences():
    return Category_Semence.objects.all()

def create_category_semence(name: str):
    return Category_Semence.objects.create(name=name)

def delete_category_semence(category_id: int):
    return Category_Semence.objects.get(id=category_id).delete()

def update_category_semence(category_id: int, name: str):
    return Category_Semence.objects.filter(id=category_id).update(name=name)
