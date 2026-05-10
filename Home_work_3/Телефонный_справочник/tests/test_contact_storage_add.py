# tests/test_contact_storage_add.py
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.contact_storage import ContactStorage


def test_add_contact_success():
    # Создаём временное имя файла, чтобы не портить настоящий справочник
    test_file = "test_contacts.txt"

    # Создаём объект хранилища с этим файлом
    storage = ContactStorage(filename=test_file)

    # Добавляем контакт
    contact = storage.add_contact(
        name="Анна",
        phone="79001234567",
        email="anna@example.com",
        comment="Друг"
    )

    # Проверяем, что у контакта есть ID
    assert "ID" in contact

    # Проверяем, что имя сохранилось правильно
    assert contact["Имя"] == "Анна"
    assert contact["Телефон"] == "79001234567"

    # Теперь загружаем все контакты из файла
    loaded = storage.load_contacts()

    # Должен быть ровно 1 контакт
    assert len(loaded) == 1
    assert loaded[0]["Имя"] == "Анна"

    # Удаляем тестовый файл после теста
    if os.path.exists(test_file):
        os.remove(test_file)


def test_validation_empty_name_or_phone():
    storage = ContactStorage()

    # Проверяем, что пустой телефон — не валиден
    assert storage.is_valid_phone("") == False
    assert storage.is_valid_phone("123") == False  # слишком коротко
    assert storage.is_valid_phone("79001234567") == True  # OK

    # Проверяем email
    assert storage.is_valid_email("") == False
    assert storage.is_valid_email("bad-email") == False
    assert storage.is_valid_email("ok@test.com") == True


def test_add_empty_contact():
    test_file = "test_empty.txt"
    storage = ContactStorage(filename=test_file)

    contact = storage.add_contact("", "", "", "")

    assert contact["Имя"] == ""
    assert contact["Телефон"] == ""

    loaded = storage.load_contacts()
    assert len(loaded) == 1

    if os.path.exists(test_file):
        os.remove(test_file)








