import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from marketplace.models import User


@pytest.mark.django_db
def test_register_user_success():
    client = APIClient()
    url = reverse('register')
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "id_categorie_user_id": 1,
        "password": "password123"
    }
    response = client.post(url, data, format='json')

    assert response.status_code == 201
    assert User.objects.filter(username="testuser").exists()
