"""
Модуль для работы с данными контактов: загрузка, сохранение, добавление, обновление, удаление.
Использует CSV для хранения данных и uuid для генерации уникальных ID.
"""

# contact_storage.py
import csv
import uuid
from typing import List, Dict, Optional


Contact = Dict[str, str]


class ContactStorage:
    """
    Класс для управления хранением контактов в CSV-файле.
    Позволяет избежать глобальных переменных и упрощает тестирование.
    """
    def __init__(self, filename: str = "ДЗ2_Контакты.txt") -> None:
        self.filename = filename

    def load_contacts(self) -> List[Contact]:
        """Загружает контакты из файла."""
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                return list(reader)
        except FileNotFoundError:
            return []
        except Exception as e:
            print(f"Ошибка при загрузке контактов: {e}")
            return []

    def write_contacts(self, contacts: List[Contact]) -> None:
        """Сохраняет контакты в файл."""
        fieldnames = ["ID", "Имя", "Телефон", "Email", "Комментарий"]
        try:
            with open(self.filename, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(contacts)
        except Exception as e:
            print(f"Ошибка при записи контактов: {e}")

    def add_contact(self, name: str, phone: str, email: str, comment: str) -> Contact:
        """Добавляет новый контакт."""
        contacts = self.load_contacts()
        new_contact = {
            "ID": str(uuid.uuid4()),
            "Имя": name.strip(),
            "Телефон": phone.strip(),
            "Email": email.strip(),
            "Комментарий": comment.strip(),
        }
        contacts.append(new_contact)
        self.write_contacts(contacts)
        return new_contact

    def update_contact(self, updated_contact: Contact) -> bool:
        """Обновляет контакт по ID."""
        contacts = self.load_contacts()
        found = False
        for i, contact in enumerate(contacts):
            if contact["ID"] == updated_contact["ID"]:
                contacts[i] = updated_contact
                found = True
                break
        if found:
            self.write_contacts(contacts)
        return found

    def delete_contact(self, contact_id: str) -> bool:
        """Удаляет контакт по ID."""
        contacts = self.load_contacts()
        initial_length = len(contacts)
        updated_contacts = [c for c in contacts if c["ID"] != contact_id]
        if len(updated_contacts) == initial_length:
            return False
        self.write_contacts(updated_contacts)
        return True

    def find_contact_by_id(self, contact_id: str) -> Optional[Contact]:
        """Находит контакт по ID."""
        contacts = self.load_contacts()
        return next((c for c in contacts if c["ID"] == contact_id), None)

    def search_contacts(self, query: str) -> List[Contact]:
        """Ищет контакты по подстроке."""
        contacts = self.load_contacts()
        query = query.lower()
        return [
            contact for contact in contacts
            if (query in contact["Имя"].lower()
                or query in contact["Телефон"].lower()
                or query in contact["Email"].lower()
                or query in contact["Комментарий"].lower())
        ]

    def is_valid_phone(self, phone: str) -> bool:
        """Проверяет номер телефона."""
        return phone.isdigit() and len(phone) >= 10

    def is_valid_email(self, email: str) -> bool:
        """Проверяет email."""
        return "@" in email and "." in email