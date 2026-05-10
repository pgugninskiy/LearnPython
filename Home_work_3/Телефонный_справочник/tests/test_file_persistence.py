import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.contact_storage import ContactStorage

def test_file_creation_and_persistence():
    test_file = "test_persistence.txt"

    # Убедимся, что файла нет
    if os.path.exists(test_file):
        os.remove(test_file)

    # Создаём хранилище — файл ещё не создан
    storage = ContactStorage(filename=test_file)

    # Загружаем — должно быть пусто
    contacts = storage.load_contacts()
    assert contacts == []  # Нет ошибки, просто пустой список

    # Добавляем контакт → файл должен создаться
    storage.add_contact("Иван", "79209998877", "ivan@test.com", "Тест")

    # Проверяем, что файл появился
    assert os.path.exists(test_file)

    # Теперь создаём новое хранилище (имитируем перезапуск программы)
    storage2 = ContactStorage(filename=test_file)
    loaded = storage2.load_contacts()

    assert len(loaded) == 1
    assert loaded[0]["Имя"] == "Иван"
    assert loaded[0]["Email"] == "ivan@test.com"

    # Удаляем файл после теста
    if os.path.exists(test_file):
        os.remove(test_file)