import csv
import uuid


# Функция загрузки контактов из файла CSV
def load_contacts():
    with open("ДЗ2_Контакты.txt", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        content = list(reader)
        return content


# Функция записи контактов в файл CSV
def write_contacts(contacts, filename="ДЗ2_Контакты.txt"):
    fieldnames = ["ID", "Имя", "Телефон", "Email", "Комментарий"]
    with open(filename, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(contacts)


# Функция добавления нового контакта
def add_contact(name, phone, email, comment):
    contacts = load_contacts()
    new_contact = {
        "ID": str(uuid.uuid4()),  # Уникальный ID
        "Имя": name,
        "Телефон": phone,
        "Email": email,
        "Комментарий": comment,
    }
    contacts.append(new_contact)
    write_contacts(contacts)
    return new_contact


def update_contact(update_contact):
    contacts = load_contacts()
    for i, contact in enumerate(contacts):
        if contact["ID"] == update_contact["ID"]:
            contacts[i] = update_contact
            break
    write_contacts(contacts)


def delete_contact(contact_id):
    """
    Удаляет контакт по ID.
    :param contact_id: int, ID контакта для удаления
    :return: True, если контакт найден и удалён, иначе False
    """
    contacts = load_contacts()  # Загружаем текущие контакты
    initial_length = len(contacts)
    # Фильтруем список, оставляя все контакты, кроме с нужным ID
    updated_contacts = [c for c in contacts if c["ID"] != contact_id]

    if len(updated_contacts) == initial_length:
        return False  # Контакт с таким ID не найден

    write_contacts(updated_contacts)  # Сохраняем обновлённый список
    return True


def is_valid_phone(phone):
    return phone.isdigit() and len(phone) >= 10


# Функция для проверки email
def is_valid_email(email):
    return "@" in email and "." in email