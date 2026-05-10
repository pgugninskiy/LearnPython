# Импортируем необходимые библиотеки
import tkinter as tk
from tkinter import ttk
from typing import Dict, List, Optional, Callable, Any
from Controller_dir.exceptions import *
from model import *


class AppButton:
    """
    Класс для создания кнопки Tkinter с заданными параметрами.

    :param master: родительский виджет (например, tk.Frame или tk.Toplevel)
    :param text: текст на кнопке
    :param command: функция, вызываемая при нажатии
    :param font: шрифт кнопки
    :param width: ширина кнопки
    :param height: высота кнопки
    :param bg: цвет фона
    :param fg: цвет текста
    :param pack_options: параметры для метода pack (отступы, выравнивание и т.д.)
    """

    def __init__(
        self,
        master: tk.Widget,
        text: str,
        command: Callable[[], None],
        font: Any,
        width: int,
        height: int,
        bg: str,
        fg: str,
        pack_options: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.btn = tk.Button(
            master,
            text=text,
            font=font,
            width=width,
            height=height,
            bg=bg,
            fg=fg,
            command=command,
        )
        pack_options = pack_options or {"pady": 5}
        self.btn.pack(**pack_options)


class AppTable:
    """
    Класс для создания таблицы (Treeview) в Tkinter с фиксированной высотой.

    :param root: родительское окно или контейнер
    :param columns: список названий столбцов
    :param show: какие элементы отображать (например, 'headings')
    :param height: высота контейнера таблицы
    """

    def __init__(
        self, root: tk.Widget, columns: List[str], show: str, height: int
    ) -> None:
        self.frame = tk.Frame(root, height=height)
        self.frame.pack(fill=tk.X, padx=2, pady=2)
        self.frame.pack_propagate(False)

        self.table = ttk.Treeview(
            self.frame,
            columns=columns,
            show=show,
        )
        self.table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=170)

    def selection(self) -> tuple:
        """Возвращает выбранные элементы таблицы."""
        return self.table.selection()

    def item(self, item_id: str) -> Dict[str, Any]:
        """
        Возвращает данные элемента по его ID.

        :param item_id: ID элемента в таблице
        :return: словарь с данными элемента
        """
        return self.table.item(item_id)

    def load_contact(self, contacts: List[Dict[str, str]]) -> None:
        """
        Загружает список контактов в таблицу.

        :param contacts: список словарей с данными контактов
        """
        for contact in contacts:
            self.table.insert(
                "",
                tk.END,
                values=(
                    contact["ID"],
                    contact["Имя"],
                    contact["Телефон"],
                    contact["Email"],
                    contact["Комментарий"],
                ),
            )

    def refresh_table(self, load_contacts: Callable[[], List[Dict[str, str]]]) -> None:
        """
        Очищает таблицу и загружает новые данные.

        :param load_contacts: функция, возвращающая список контактов
        """
        for row in self.table.get_children():
            self.table.delete(row)

        contacts = load_contacts()
        for contact in contacts:
            self.table.insert(
                "",
                tk.END,
                values=(
                    contact["ID"],
                    contact["Имя"],
                    contact["Телефон"],
                    contact["Email"],
                    contact["Комментарий"],
                ),
            )


class AppLabel:
    """
    Класс для создания текстовой метки (Label) в Tkinter.

    :param root: родительский виджет
    :param text: начальный текст метки
    :param fg: цвет текста (опционально)
    """

    def __init__(self, root: tk.Widget, text: str, fg: Optional[str] = None) -> None:
        self.root = tk.Label(root, text=text, font=("Arial", 18), fg=fg)
        self.root.pack(anchor="c", padx=10)

    def destroy(self) -> None:
        """Удаляет метку из интерфейса."""
        self.root.destroy()

    def clear_status(self) -> None:
        """Очищает текст метки."""
        self.root.config(text="")

    def update_text(self, text: str, fg: Optional[str] = None) -> None:
        """
        Обновляет текст и, опционально, цвет метки.

        :param text: новый текст
        :param fg: новый цвет текста (если указан)
        """
        self.root.config(text=text)
        if fg is not None:
            self.root.config(fg=fg)


class AppEntry:
    """
    Класс для создания поля ввода (Entry) в Tkinter.

    :param root: родительский виджет
    :param font: шрифт поля ввода
    :param width: ширина поля
    """

    def __init__(self, root: tk.Widget, font: Any, width: int) -> None:
        self.root = tk.Entry(root, font=font, width=width)
        self.root.pack(pady=5)

    def get(self) -> str:
        """Возвращает текущее значение поля ввода."""
        return self.root.get()

    def delete(self) -> None:
        """Очищает поле ввода."""
        self.root.delete(0, tk.END)


class AppWindowModal:
    """
    Модальное окно для редактирования контакта или подтверждения действия.

    :param parent: родительское окно (Toplevel)
    :param contact_data: данные контакта (в режиме редактирования)
    :param on_save_callback: функция, вызываемая после сохранения
    :param mode: режим окна ('edit' или 'confirm')
    :param confirm_message: сообщение для режима подтверждения
    :param on_confirm: функция, вызываемая при подтверждении
    """

    def __init__(
        self,
        parent: tk.Toplevel,
        contact_data: Optional[Dict[str, str]] = None,
        on_save_callback: Optional[Callable[[], None]] = None,
        mode: str = "edit",
        confirm_message: Optional[str] = None,
        on_confirm: Optional[Callable[[], None]] = None,
    ) -> None:
        self.parent = parent
        self.contact_data = contact_data
        self.on_save_callback = on_save_callback
        self.mode = mode
        self.confirm_message = confirm_message
        self.on_confirm = on_confirm
        self.entries: Dict[str, tk.Entry] = {}
        self.create_window()
        self.storage = ContactStorage()

    def create_window(self) -> None:
        """Создаёт и настраивает содержимое модального окна в зависимости от режима."""
        if self.mode == "confirm":
            self.parent.title("Подтверждение")
            self.parent.geometry("450x250")
        else:
            self.parent.title("Редактировать контакт")
            self.parent.geometry("750x380")

        self.parent.resizable(False, False)
        self.parent.grab_set()
        self.parent.focus_set()

        if self.mode == "confirm":
            tk.Label(
                self.parent,
                text=self.confirm_message,
                font=("Arial", 12),
                wraplength=350,
            ).pack(pady=20)
            AppButton(
                self.parent,
                text="Да, удалить",
                font=("Arial", 12),
                width=15,
                height=2,
                bg="red",
                fg="white",
                command=lambda: (self.on_confirm(), self.parent.destroy()),
            )
            AppButton(
                self.parent,
                text="Нет, оставь",
                font=("Arial", 12),
                width=15,
                height=2,
                bg="gray",
                fg="white",
                command=self.parent.destroy,
            )
        else:
            fields = ["Имя", "Телефон", "Email", "Комментарий"]
            for field in fields:
                tk.Label(self.parent, text=f"{field}:", font=("Arial", 11)).pack(
                    anchor="w", padx=20, pady=(10, 0)
                )
                entry = tk.Entry(self.parent, width=50, font=("Arial", 10))
                entry.pack(padx=20, pady=5)
                entry.insert(0, self.contact_data.get(field, "") if self.contact_data else "")
                self.entries[field] = entry

            AppButton(
                self.parent,
                text="Сохранить изменения",
                font=("Arial", 12),
                width=20,
                height=2,
                bg="green",
                fg="white",
                command=self.save_edits,
            )

    def save_edits(self) -> None:
        """Сохраняет изменения контакта после валидации полей."""
        # Удаляем предыдущее сообщение об ошибке, если оно есть
        if hasattr(self, 'error_label') and self.error_label:
            self.error_label.destroy()
            self.error_label = None

        try:
            updated_data = {
                "ID": self.contact_data["ID"],
                "Имя": self.entries["Имя"].get().strip(),
                "Телефон": self.entries["Телефон"].get().strip(),
                "Email": self.entries["Email"].get().strip(),
                "Комментарий": self.entries["Комментарий"].get().strip(),
            }

            if not updated_data["Имя"] or not updated_data["Телефон"]:
                raise EmptyFieldError()
            if not self.storage.is_valid_phone(updated_data["Телефон"]):
                raise InvalidPhoneError()
            if updated_data["Email"] and not self.storage.is_valid_email(updated_data["Email"]):
                raise InvalidEmailError()

            success = self.storage.update_contact(updated_data)

            if success and self.on_save_callback:
                self.on_save_callback()

            self.parent.destroy()

        except (EmptyFieldError, InvalidPhoneError, InvalidEmailError) as e:
            # Показываем ошибку под кнопкой
            self.error_label = AppLabel(self.parent, text=str(e), fg="red")
            self.error_label.root.pack(pady=5)
        except Exception as e:
            # На случай других ошибок
            self.error_label = AppLabel(self.parent, text=f"Ошибка: {str(e)}", fg="red")
            self.error_label.root.pack(pady=5)

    def confirm(self) -> None:
        """Вызывается при подтверждении действия в режиме 'confirm'."""
        if self.on_confirm:
            self.on_confirm()
            self.parent.destroy()


# --- Миксины для разделения функциональности ---

class StartScreenMixin:
    """Миксин для отображения стартового экрана приложения."""

    def show_start_screen(self: 'App') -> None:
        """
        Очищает экран и отображает главное меню с кнопками действий.
        """
        self.clear_screen()
        buttons = [
            ("Показать все контакты", self.get_all_contacts),
            ("Создать контакт", self.create_contact),
            ("Найти контакт", self.search_contact),
            ("Изменить / удалить контакт", self.edit_contact),
            ("Выход", self.root.destroy),
        ]

        for text, command in buttons:
            bg_color = "red" if text == "Выход" else "black"
            AppButton(
                self.root,
                text=text,
                font=("Courier New", 15, "bold"),
                width=75,
                height=7,
                bg=bg_color,
                fg="white",
                command=command,
            )


class ContactScreenMixin:
    """Миксин для отображения всех контактов."""

    def get_all_contacts(self: 'App') -> None:
        """Открывает контроллер для отображения всех контактов."""
        from Controller_dir.controller_v2 import ContactController
        ctrl = ContactController(self)
        ctrl.get_all_contacts()


class CreateContactScreenMixin:
    """Миксин для создания нового контакта."""

    def create_contact(self: 'App') -> None:
        """Открывает контроллер для создания нового контакта."""
        from Controller_dir.controller_v2 import ContactController
        ctrl = ContactController(self)
        ctrl.create_contact()


class SearchContactScreenMixin:
    """Миксин для поиска контакта."""

    def search_contact(self: 'App') -> None:
        """Открывает контроллер для поиска контакта."""
        from Controller_dir.controller_v2 import ContactController
        ctrl = ContactController(self)
        ctrl.search_contact()


class EditContactScreenMixin:
    """Миксин для редактирования контакта."""

    def edit_contact(self: 'App') -> None:
        """Открывает контроллер для редактирования контакта."""
        from Controller_dir.controller_v2 import ContactController
        ctrl = ContactController(self)
        ctrl.edit_contact()


# --- Основной класс приложения ---

class App(StartScreenMixin, ContactScreenMixin, CreateContactScreenMixin,
          SearchContactScreenMixin, EditContactScreenMixin):
    """
    Основной класс приложения — телефонный справочник с графическим интерфейсом.

    Использует миксины для разделения функциональности.
    """

    def __init__(self, root: tk.Tk) -> None:
        """
        Инициализирует главное окно приложения.

        :param root: главное окно Tkinter
        """
        self.root = root
        self.root.title("Телефонный_справочник")
        self.root.geometry("1000x850")
        self.root.configure(bg="black")
        self.show_start_screen()

    def clear_screen(self) -> None:
        """Удаляет все виджеты из главного окна."""
        for widget in self.root.winfo_children():
            widget.destroy()