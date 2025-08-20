from core.models import Product

import pytest


@pytest.mark.django_db
def test_create_product():
    product = Product.objects.create(name="Riz", price=1000)
    assert product.name == "Riz"
    assert product.price == 1000
    assert Product.objects.count() == 1

import pytest
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_list_products():
    client = APIClient()
    response = client.get("/api/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
