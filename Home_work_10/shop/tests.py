# shop/tests.py
import pytest
from django.core.exceptions import ValidationError
from shop.models import Product
from shop.forms import ProductForm


# ==========================================
# ТЕСТЫ ДЛЯ МОДЕЛИ (CRUD операции)
# ==========================================

@pytest.mark.django_db
def test_product_create():
    """Тест создания товара (CREATE)"""
    product = Product.objects.create(
        name="Тестовый товар",
        description="Описание теста",
        price=100.50
    )
    assert product.pk is not None
    assert product.name == "Тестовый товар"
    assert product.price == 100.50


@pytest.mark.django_db
def test_product_read():
    """Тест чтения товара (READ)"""
    product = Product.objects.create(
        name="Товар для чтения",
        description="Описание",
        price=200
    )
    # Получаем товар из БД
    fetched_product = Product.objects.get(pk=product.pk)
    assert fetched_product.name == "Товар для чтения"
    assert fetched_product.price == 200


@pytest.mark.django_db
def test_product_update():
    """Тест обновления товара (UPDATE)"""
    product = Product.objects.create(
        name="Старое название",
        description="Описание",
        price=100
    )
    # Меняем данные
    product.name = "Новое название"
    product.price = 500
    product.save()
    
    # Проверяем, что изменения сохранились
    updated = Product.objects.get(pk=product.pk)
    assert updated.name == "Новое название"
    assert updated.price == 500


@pytest.mark.django_db
def test_product_delete():
    """Тест удаления товара (DELETE)"""
    product = Product.objects.create(
        name="Товар на удаление",
        description="Описание",
        price=100
    )
    product_pk = product.pk
    product.delete()
    
    # Проверяем, что товар удален
    assert not Product.objects.filter(pk=product_pk).exists()


@pytest.mark.django_db
def test_product_str():
    """Тест строкового представления товара"""
    product = Product.objects.create(
        name="Товар для str",
        description="Описание",
        price=100
    )
    assert str(product) == "Товар для str"


# ==========================================
# ТЕСТЫ ДЛЯ ФОРМЫ (валидация)
# ==========================================

@pytest.mark.django_db
def test_product_form_valid():
    """Тест валидной формы"""
    form_data = {
        'name': 'Валидный товар',
        'description': 'Описание',
        'price': 100,
    }
    form = ProductForm(data=form_data)
    assert form.is_valid()


@pytest.mark.django_db
def test_product_form_invalid_price():
    """Тест формы с отрицательной ценой (должна быть невалидной)"""
    form_data = {
        'name': 'Товар с плохой ценой',
        'description': 'Описание',
        'price': -100,
    }
    form = ProductForm(data=form_data)
    assert not form.is_valid()
    assert 'price' in form.errors


@pytest.mark.django_db
def test_product_form_missing_name():
    """Тест формы без названия (обязательное поле)"""
    form_data = {
        'description': 'Описание',
        'price': 100,
    }
    form = ProductForm(data=form_data)
    assert not form.is_valid()
    assert 'name' in form.errors