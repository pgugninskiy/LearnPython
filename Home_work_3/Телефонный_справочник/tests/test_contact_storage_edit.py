import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.contact_storage import ContactStorage

def test_update_contact_success():
    test_file = "test_edit.txt"
    storage = ContactStorage(filename=test_file)

    # Сначала добавим контакт
    contact = storage.add_contact("Старое Имя", "79001112233", "old@test.com", "Старый коммент")
    contact_id = contact["ID"]

    # Теперь обновим его
    updated = {
        "ID": contact_id,
        "Имя": "Новое Имя",
        "Телефон": "79104445566",
        "Email": "new@test.com",
        "Комментарий": "Новый коммент"
    }

    success = storage.update_contact(updated)
    assert success == True

    # Проверим, что изменения сохранились
    loaded = storage.load_contacts()
    assert len(loaded) == 1
    assert loaded[0]["Имя"] == "Новое Имя"
    assert loaded[0]["Телефон"] == "79104445566"

    # Удаляем файл
    if os.path.exists(test_file):
        os.remove(test_file)


def test_update_nonexistent_contact():
    test_file = "test_edit_not_found.txt"
    storage = ContactStorage(filename=test_file)

    # Добавим один контакт
    contact = storage.add_contact("Анна", "79001234567", "", "")

    # Попробуем обновить контакт с несуществующим ID
    fake_updated = {
        "ID": "несуществующий-id",
        "Имя": "Борис",
        "Телефон": "79998887766",
        "Email": "",
        "Комментарий": ""
    }

    success = storage.update_contact(fake_updated)
    assert success == False  # Не должно обновиться

    # Убедимся, что оригинал не изменился
    loaded = storage.load_contacts()
    assert len(loaded) == 1
    assert loaded[0]["Имя"] == "Анна"

    if os.path.exists(test_file):
        os.remove(test_file)

def test_validation_during_edit():
    storage = ContactStorage()

    # Проверка телефона
    assert storage.is_valid_phone("79001234567") == True   # 11 цифр
    assert storage.is_valid_phone("9001234567") == True    # 10 цифр — OK
    assert storage.is_valid_phone("123") == False          # слишком коротко
    assert storage.is_valid_phone("abc") == False          # не цифры

    # Проверка email
    assert storage.is_valid_email("user@domain.com") == True
    assert storage.is_valid_email("bad-email") == False
    assert storage.is_valid_email("") == False             # пустой — не валиден

    # Пустые поля — не разрешены (это проверяется в AppWindowModal, но мы можем имитировать)
    name = ""
    phone = "79001234567"
    assert not (name and phone)  # если имя пустое — ошибка

def test_partial_update():
    test_file = "test_partial.txt"
    storage = ContactStorage(filename=test_file)

    contact = storage.add_contact("Иван", "79201112233", "ivan@test.ru", "Старый")
    contact_id = contact["ID"]

    # Обновляем только комментарий
    updated = {
        "ID": contact_id,
        "Имя": "Иван",               # то же самое
        "Телефон": "79201112233",    # то же самое
        "Email": "ivan@test.ru",     # то же самое
        "Комментарий": "Новый коммент"
    }

    success = storage.update_contact(updated)
    assert success == True

    loaded = storage.load_contacts()
    assert loaded[0]["Комментарий"] == "Новый коммент"
    assert loaded[0]["Имя"] == "Иван"  # остальное не изменилось

    if os.path.exists(test_file):
        os.remove(test_file)