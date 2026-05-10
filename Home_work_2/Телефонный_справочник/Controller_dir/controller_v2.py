"""
Модуль контроллера для приложения телефонного справочника.

Класс ContactController координирует взаимодействие между моделью (model) и представлением (view).
Отвечает за логику отображения, создания, поиска, редактирования и удаления контактов.
"""

from typing import List, Dict, Optional
import tkinter as tk

# Импорты из других модулей приложения
from model import ContactStorage
from view import (
    AppButton,
    AppTable,
    AppLabel,
    AppEntry,
    AppWindowModal,
)
from .exceptions import EmptyFieldError, InvalidPhoneError, InvalidEmailError


# Тип для контакта
Contact = Dict[str, str]


class ContactController:
    """
    Контроллер для управления контактами.

    Обрабатывает пользовательские действия: просмотр, добавление, поиск, редактирование и удаление.
    Взаимодействует с моделью (model.py) и представлением (view.py).
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
        Проверяет введённые данные и сохраняет контакт при успешной валидации.
        """
        self.app.clear_screen()
        status_label: List[Optional[AppLabel]] = [None]  # Хак для nonlocal в замыкании

        def clear_status() -> None:
            """Удаляет текущее сообщение статуса."""
            if status_label[0] is not None:
                status_label[0].destroy()
                status_label[0] = None

        def save_new_contact() -> None:
            """Обработчик кнопки 'Сохранить' — валидирует и сохраняет контакт."""
            clear_status()
            name = entry_name.get().strip()
            phone = entry_phone.get().strip()
            email = entry_email.get().strip()
            comment = entry_comment.get().strip()

            try:
                if not name or not phone:
                    raise EmptyFieldError()
                if not self.storage.is_valid_phone(phone):
                    raise InvalidPhoneError()
                if email and not self.storage.is_valid_email(email):
                    raise InvalidEmailError()

                self.storage.add_contact(name=name, phone=phone, email=email, comment=comment)

                # Очистка полей ввода
                entry_name.delete()
                entry_phone.delete()
                entry_email.delete()
                entry_comment.delete()

                # Показ успешного сообщения
                status_label[0] = AppLabel(self.root, text="Данные сохранены!", fg="green")

            except (EmptyFieldError, InvalidPhoneError, InvalidEmailError) as e:
                status_label[0] = AppLabel(self.root, text=str(e), fg="red")
            except Exception as e:
                status_label[0] = AppLabel(self.root, text=f"Ошибка: {str(e)}", fg="red")
                print(f"Неизвестная ошибка при сохранении контакта: {e}")

        # Интерфейс ввода
        AppLabel(self.root, text="Имя:")
        entry_name = AppEntry(self.root, ("Arial", 12), 80)

        AppLabel(self.root, text="Телефон:")
        entry_phone = AppEntry(self.root, ("Arial", 12), 80)

        AppLabel(self.root, text="Email:")
        entry_email = AppEntry(self.root, ("Arial", 12), 80)

        AppLabel(self.root, text="Комментарий:")
        entry_comment = AppEntry(self.root, ("Arial", 12), 80)

        # Кнопки
        AppButton(
            self.root,
            text="Сохранить",
            font=("Arial", 12),
            width=15,
            height=2,
            bg="black",
            fg="white",
            command=save_new_contact,
        )

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

    def search_contact(self) -> None:
        """
        Открывает форму поиска контактов.
        Позволяет искать по имени, телефону, email или комментарию.
        """
        self.app.clear_screen()
        columns = ("ID", "Имя", "Телефон", "Email", "Комментарий")
        tree = AppTable(self.root, columns=columns, show="headings", height=450)

        tree.table.column("ID", width=0, stretch=tk.NO)
        tree.table.heading("ID", text="ID")

        contacts: List[Contact] = self.storage.load_contacts()
        tree.load_contact(contacts)

        # Поля ввода для фильтрации
        AppLabel(self.root, text="Имя:")
        entry_name = AppEntry(self.root, ("Arial", 12), 80)

        AppLabel(self.root, text="Телефон:")
        entry_phone = AppEntry(self.root, ("Arial", 12), 80)

        AppLabel(self.root, text="Email:")
        entry_email = AppEntry(self.root, ("Arial", 12), 80)

        AppLabel(self.root, text="Комментарий:")
        entry_comment = AppEntry(self.root, ("Arial", 12), 80)

        def perform_search() -> None:
            """Фильтрует контакты по введённым критериям."""
            # Очистка таблицы
            for item in tree.table.get_children():
                tree.table.delete(item)

            # Получение значений фильтров
            name_query = entry_name.get().strip().lower()
            phone_query = entry_phone.get().strip().lower()
            email_query = entry_email.get().strip().lower()
            comment_query = entry_comment.get().strip().lower()

            # Фильтрация
            results = [
                c for c in contacts
                if (not name_query or name_query in c["Имя"].lower()) and
                   (not phone_query or phone_query in c["Телефон"].lower()) and
                   (not email_query or email_query in c["Email"].lower()) and
                   (not comment_query or comment_query in c.get("Комментарий", "").lower())
            ]
            tree.load_contact(results)

        # Кнопки
        AppButton(
            self.root,
            text="Поиск",
            font=("Arial", 12),
            width=15,
            height=2,
            bg="blue",
            fg="white",
            command=perform_search,
        )

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

    def edit_contact(self) -> None:
        """
        Открывает форму редактирования и удаления контактов.
        Позволяет выбрать контакт, изменить его или удалить с подтверждением.
        """
        self.app.clear_screen()
        columns = ("ID", "Имя", "Телефон", "Email", "Комментарий")
        tree = AppTable(self.root, columns=columns, show="headings", height=620)

        tree.table.column("ID", width=0, stretch=tk.NO)
        tree.table.heading("ID", text="ID")

        contacts: List[Contact] = self.storage.load_contacts()
        tree.load_contact(contacts)

        # Хранение ссылки на последнюю метку
        status_label: List[Optional[AppLabel]] = [None]

        def open_edit_window():
            """Открывает модальное окно для редактирования выбранного контакта."""
            selected_items = tree.selection()

            if not selected_items:
                if status_label[0]:
                    status_label[0].update_text("Выберите контакт для редактирования!", fg="red")
                else:
                    status_label[0] = AppLabel(self.root, text="Выберите контакт для редактирования!", fg="red")
                return

            selected_item = selected_items[0]
            values = tree.item(selected_item)["values"]
            contact_id = values[0]
            contact_data = next((c for c in contacts if c["ID"] == contact_id), None)
            contact_name = values[1]

            if not contact_data:
                if status_label[0]:
                    status_label[0].update_text("Контакт не найден!", fg="red")
                else:
                    status_label[0] = AppLabel(self.root, text="Контакт не найден!", fg="red")
                return

            def on_save_success() -> None:
                """Вызывается при успешном сохранении — обновляет таблицу и показывает статус."""
                tree.refresh_table(self.storage.load_contacts)
                message = f"Контакт '{contact_name}' обновлен"
                if status_label[0]:
                    status_label[0].update_text(message, fg="green")
                else:
                    status_label[0] = AppLabel(self.root, text=message, fg="green")

            edit_win = tk.Toplevel(self.root)
            AppWindowModal(
                parent=edit_win,
                contact_data=contact_data,
                on_save_callback=on_save_success,
            )

        def confirm_delete() -> None:
            """Запускает процесс удаления контакта с подтверждением."""
            selected_items = tree.selection()

            if not selected_items:
                if status_label[0]:
                    status_label[0].update_text("Выберите контакт для удаления!", fg="red")
                else:
                    status_label[0] = AppLabel(self.root, text="Выберите контакт для удаления!", fg="red")
                return

            selected_item = selected_items[0]
            values = tree.item(selected_item)["values"]
            contact_id = values[0]
            contact_name = values[1]

            def do_delete() -> None:
                """Удаляет контакт после подтверждения."""
                success = self.storage.delete_contact(contact_id)
                message = f"Контакт '{contact_name}' удалён!" if success else "Контакт не найден!"
                fg = "green" if success else "red"

                if status_label[0]:
                    status_label[0].update_text(message, fg=fg)
                else:
                    status_label[0] = AppLabel(self.root, text=message, fg=fg)

                if success:
                    tree.refresh_table(self.storage.load_contacts)

            confirm_win = tk.Toplevel(self.root)
            AppWindowModal(
                parent=confirm_win,
                mode="confirm",
                confirm_message=f"Удалить контакт '{contact_name}'?",
                on_confirm=do_delete,
            )

        # Кнопки действий
        AppButton(
            self.root,
            text="Изменить",
            font=("Arial", 12),
            width=15,
            height=2,
            bg="black",
            fg="white",
            command=open_edit_window,
        )

        AppButton(
            self.root,
            text="Удалить",
            font=("Arial", 12),
            width=15,
            height=2,
            bg="red",
            fg="white",
            command=confirm_delete,
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
