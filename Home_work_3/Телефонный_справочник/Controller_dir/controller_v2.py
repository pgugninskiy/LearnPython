"""
Модуль контроллера для приложения телефонного справочника.

Класс ContactController координирует взаимодействие между моделью (model) и представлением (view_forms).
Отвечает за логику отображения, создания, поиска, редактирования и удаления контактов.
"""

from typing import List, Dict, Optional
import tkinter as tk

# Импорты из других модулей приложения
from model.contact_storage import ContactStorage
from view_forms.view import (
    AppButton,
    AppTable,
    AppLabel,
    AppEntry,
    AppWindowModal,
)
from view_forms.forms.create_form import CreateContactForm
from view_forms.forms.search_form import SearchContactForm
from .exceptions import EmptyFieldError, InvalidPhoneError, InvalidEmailError


# Тип для контакта
Contact = Dict[str, str]


class ContactController:
    """
    Контроллер для управления контактами.

    Обрабатывает пользовательские действия: просмотр, добавление, поиск, редактирование и удаление.
    Взаимодействует с моделью (contact_storage.py) и представлением (view_forms.py).
    """

    def __init__(self, app_instance: 'App', filename: str = "ДЗ2_Контакты.txt") -> None:
        """
        Инициализирует контроллер.

        :param app_instance: Экземпляр основного приложения (App), чтобы иметь доступ к его методам (например, clear_screen).
        """
        self.app = app_instance
        self.root: tk.Tk = app_instance.root
        self.storage = ContactStorage(filename)

    def get_all_contacts(self) -> None:
        """
        Отображает все сохранённые контакты в таблице.
        """
        self.app.clear_screen()
        columns = ("ID", "Имя", "Телефон", "Email", "Комментарий")
        tree = AppTable(self.root, columns=columns, show="headings", height=800)

        # Скрываем колонку ID, но оставляем её для внутреннего использования
        tree.table.column("ID", width=0, stretch=tk.NO)
        tree.table.heading("ID", text="ID")

        contacts = self.storage.load_contacts()
        tree.load_contact(contacts)

        AppButton(
            self.root,
            text="Назад",
            font=("Arial", 12),
            width=15,
            height=2,
            bg="red",
            fg="white",
            command=self.app.show_start_screen,
        )

    def create_contact(self) -> None:
        """
        Открывает форму для создания нового контакта.
        Вся логика UI теперь в CreateContactForm.
        """
        self.app.clear_screen()

        def handle_save(name: str, phone: str, email: str, comment: str) -> None:
            """Обработка сохранения — здесь живёт валидация и запись."""
            try:
                # Валидация
                if not name or not phone:
                    raise EmptyFieldError()
                if not self.storage.is_valid_phone(phone):
                    raise InvalidPhoneError()
                if email and not self.storage.is_valid_email(email):
                    raise InvalidEmailError()

                # Сохранение
                self.storage.add_contact(name=name, phone=phone, email=email, comment=comment)

                # Показ успеха
                form.show_message("Данные сохранены!", color="green")


            except (EmptyFieldError, InvalidPhoneError, InvalidEmailError) as e:
                form.show_message(str(e), color="red")
            except Exception as e:
                print(f"Неизвестная ошибка: {e}")
                form.show_message("Произошла ошибка при сохранении.", color="red")

        # Создаём форму и передаём ей обработчики
        form = CreateContactForm(
            parent=self.root,
            on_save=handle_save,
            on_cancel=self.app.show_start_screen,
        )

    def search_contact(self) -> None:
        """
        Открывает форму поиска контактов.
        Таблица создаётся один раз, а затем обновляется при каждом поиске.
        """
        self.app.clear_screen()

        # Создаём таблицу один раз (она будет обновляться)
        columns = ("ID", "Имя", "Телефон", "Email", "Комментарий")
        tree = AppTable(self.root, columns=columns, show="headings", height=450)
        tree.table.column("ID", width=0, stretch=tk.NO)
        tree.table.heading("ID", text="ID")

        # Загружаем все контакты один раз (для фильтрации)
        all_contacts = self.storage.load_contacts()

        def handle_search(name: str, phone: str, email: str, comment: str) -> None:
            """Фильтрует контакты и обновляет таблицу."""
            # Очистка таблицы
            for item in tree.table.get_children():
                tree.table.delete(item)

            # Фильтрация
            results = [
                c for c in all_contacts
                if (not name or name.lower() in c["Имя"].lower())
                   and (not phone or phone.lower() in c["Телефон"].lower())
                   and (not email or email.lower() in c["Email"].lower())
                   and (not comment or comment.lower() in c.get("Комментарий", "").lower())
            ]

            # Загрузка результатов
            tree.load_contact(results)

        # Создаём форму поиска
        SearchContactForm(
            parent=self.root,
            on_search=handle_search,
            on_cancel=self.app.show_start_screen,
        )

    def edit_contact(self) -> None:
        """
        Открывает экран для редактирования или удаления контактов.
        Пользователь выбирает контакт в таблице, затем нажимает "Изменить" или "Удалить".
        """
        self.app.clear_screen()

        # === 1. Создаём таблицу ===
        columns = ("ID", "Имя", "Телефон", "Email", "Комментарий")
        tree = AppTable(self.root, columns=columns, show="headings", height=620)
        tree.table.column("ID", width=0, stretch=tk.NO)
        tree.table.heading("ID", text="ID")

        contacts = self.storage.load_contacts()
        tree.load_contact(contacts)

        # === 2. Статус-метка (для ошибок/успеха) ===
        status_label: List[Optional[AppLabel]] = [None]

        def show_message(text: str, fg: str = "red") -> None:
            if status_label[0]:
                status_label[0].update_text(text, fg=fg)
            else:
                status_label[0] = AppLabel(self.root, text=text, fg=fg)

        # === 3. Функция: получить выбранный контакт ===
        def get_selected_contact() -> Optional[Dict[str, str]]:
            selected_items = tree.selection()
            if not selected_items:
                show_message("Выберите контакт для действия!")
                return None

            item_id = selected_items[0]
            values = tree.item(item_id)["values"]
            contact_id = values[0]
            contact_name = values[1]

            contact = next((c for c in contacts if c["ID"] == contact_id), None)
            if not contact:
                show_message("Контакт не найден в данных!")
                return None

            return contact

        # === 4. Обработчик "Изменить" ===
        def handle_edit() -> None:
            contact = get_selected_contact()
            if not contact:
                return

            def on_save_success() -> None:
                tree.refresh_table(self.storage.load_contacts)
                show_message(f"Контакт '{contact['Имя']}' обновлён!", fg="green")

            edit_win = tk.Toplevel(self.root)
            AppWindowModal(
                parent=edit_win,
                contact_data=contact,
                on_save_callback=on_save_success,
                mode="edit"
            )

        # === 5. Обработчик "Удалить" ===
        def handle_delete() -> None:
            contact = get_selected_contact()
            if not contact:
                return

            def do_delete() -> None:
                success = self.storage.delete_contact(contact["ID"])
                if success:
                    tree.refresh_table(self.storage.load_contacts)
                    show_message(f"Контакт '{contact['Имя']}' удалён!", fg="green")
                else:
                    show_message("Не удалось удалить контакт.", fg="red")

            confirm_win = tk.Toplevel(self.root)
            AppWindowModal(
                parent=confirm_win,
                mode="confirm",
                confirm_message=f"Удалить контакт '{contact['Имя']}'?",
                on_confirm=do_delete,
            )

        # === 6. Кнопки ===
        AppButton(
            self.root,
            text="Изменить",
            font=("Arial", 12),
            width=15,
            height=2,
            bg="black",
            fg="white",
            command=handle_edit,
        )
        AppButton(
            self.root,
            text="Удалить",
            font=("Arial", 12),
            width=15,
            height=2,
            bg="red",
            fg="white",
            command=handle_delete,
        )
        AppButton(
            self.root,
            text="Назад",
            font=("Arial", 12),
            width=15,
            height=2,
            bg="gray",
            fg="white",
            command=self.app.show_start_screen,
        )
