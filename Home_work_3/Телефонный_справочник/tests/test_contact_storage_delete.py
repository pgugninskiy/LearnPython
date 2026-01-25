import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.contact_storage import ContactStorage

def test_delete_contact_success():
    test_file = "test_delete_ok.txt"
    storage = ContactStorage(filename=test_file)

    # Добавим контакт
    contact = storage.add_contact("Анна", "79001234567", "", "")
    contact_id = contact["ID"]

    # Удалим его
    result = storage.delete_contact(contact_id)
    assert result == True  # Удаление прошло успешно

    # Проверим, что контакт исчез
    contacts = storage.load_contacts()
    assert len(contacts) == 0

    # Удалим временный файл
    if os.path.exists(test_file):
        os.remove(test_file)


def test_delete_contact_with_invalid_id():
    test_file = "test_delete_bad_id.txt"
    storage = ContactStorage(filename=test_file)

    # Добавим один контакт
    storage.add_contact("Борис", "79101112233", "", "")

    # Попробуем удалить по несуществующему ID
    fake_id = "несуществующий-id-123"
    result = storage.delete_contact(fake_id)
    assert result == False  # Удаление не удалось

    # Убедимся, что контакт остался
    contacts = storage.load_contacts()
    assert len(contacts) == 1
    assert contacts[0]["Имя"] == "Борис"

    if os.path.exists(test_file):
        os.remove(test_file)