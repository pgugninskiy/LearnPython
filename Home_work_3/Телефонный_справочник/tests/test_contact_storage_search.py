import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.contact_storage import ContactStorage

def test_search_by_name():
    # Имя временного файла
    test_file = "test_search.txt"
    storage = ContactStorage(filename=test_file)

    # Добавим пару контактов вручную (через add_contact)
    storage.add_contact("Анна Петрова", "79001112233", "anna@test.ru", "Друг")
    storage.add_contact("Борис Сидоров", "79104445566", "boris@work.com", "Коллега")

    # Ищем по имени "Анна"
    results = storage.search_contacts("Анна")
    assert len(results) == 1
    assert results[0]["Имя"] == "Анна Петрова"

    # Удаляем тестовый файл
    if os.path.exists(test_file):
        os.remove(test_file)


def test_search_by_phone():
    test_file = "test_search_phone.txt"
    storage = ContactStorage(filename=test_file)

    storage.add_contact("Мария", "79201234567", "maria@mail.ru", "")
    storage.add_contact("Иван", "79309876543", "ivan@box.com", "Боксёр")

    # Ищем по части номера телефона
    results = storage.search_contacts("920123")
    assert len(results) == 1
    assert results[0]["Имя"] == "Мария"

    # Удаляем файл
    if os.path.exists(test_file):
        os.remove(test_file)


def test_general_search():
    test_file = "test_general.txt"
    storage = ContactStorage(filename=test_file)

    storage.add_contact("Ольга", "79501112233", "olga@company.org", "HR-менеджер")

    # Ищем по части email
    results = storage.search_contacts("company")
    assert len(results) == 1
    assert "HR-менеджер" in results[0]["Комментарий"]

    # Ищем по части комментария
    results2 = storage.search_contacts("менеджер")
    assert len(results2) == 1
    assert results2[0]["Имя"] == "Ольга"

    if os.path.exists(test_file):
        os.remove(test_file)


def test_search_nonexistent_contact():
    test_file = "test_not_found.txt"
    storage = ContactStorage(filename=test_file)

    # Добавим один контакт
    storage.add_contact("Сергей", "79998887766", "sergey@example.com", "")

    # Ищем то, чего нет
    results = storage.search_contacts("НесуществующийИмя")
    assert len(results) == 0  # Ничего не найдено

    # Ищем несуществующий номер
    results2 = storage.search_contacts("0000000000")
    assert len(results2) == 0

    if os.path.exists(test_file):
        os.remove(test_file)