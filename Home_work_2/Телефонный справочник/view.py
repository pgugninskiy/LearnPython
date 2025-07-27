# Импортируем необходимые библиотеки
import tkinter as tk
from tkinter import ttk  # Для работы с таблицами (Treeview)
from Controller_dir.exceptions import *
from model import *

# --- Вспомогательные классы для упрощения работы с tkinter ---

# Класс для создания кнопок с заданными параметрами
class AppButton:
    def __init__(
        self, master, text, command, font, width, height, bg, fg, pack_options=None
    ):
        # Создаем кнопку с заданными параметрами
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
        # Если pack_options не переданы, используем стандартные значения
        pack_options = pack_options or {"pady": 5}
        self.btn.pack(**pack_options)  # Распаковываем параметры и позиционируем кнопку


# Класс для создания таблицы с заданными параметрами
class AppTable:
    def __init__(self, root, columns, show, height):
        # Создаем контейнер (Frame) с фиксированной высотой
        self.frame = tk.Frame(root, height=height)
        self.frame.pack(fill=tk.X, padx=2, pady=2)
        self.frame.pack_propagate(False)  # Отключаем авто-изменение размера Frame

        # Создаем таблицу внутри Frame
        self.table = ttk.Treeview(
            self.frame, columns=columns, show=show  # show — какие части отображать (например, заголовки)
        )
        self.table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)  # Позиционируем таблицу

        # Настраиваем заголовки и ширину столбцов
        for col in columns:
            self.table.heading(col, text=col)  # Устанавливаем текст заголовка
            self.table.column(col, width=170)  # Фиксируем ширину столбца

    def selection(self):
        return self.table.selection()

    def item(self, item_id):
        return self.table.item(item_id)

    def load_contact(self, contacts):
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

    def refresh_table(self, load_contacts):
        """
        Обновляет таблицу с использованием функции загрузки контактов.

        :param load_contacts_func: функция, возвращающая список контактов
        """
        # Очистка текущих строк
        for row in self.table.get_children():
            self.table.delete(row)

        # Загрузка новых данных
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

# Класс для создания меток (Label)
class AppLabel:
    def __init__(self, root, text, fg=None):
        # Создаем текстовую метку
        self.root = tk.Label(root, text=text, font=("Arial", 18), fg=fg)
        self.root.pack(anchor="c", padx=10)  # Центрируем по горизонтали

    # Метод для удаления метки
    def destroy(self):
        return self.root.destroy()

    # Метод для очистки текста метки
    def clear_status(self):
        self.root.config(text="")

    # Новый метод для обновления текста и цвета метки
    def update_text(self, text, fg=None):
        self.root.config(text=text)
        if fg is not None:
            self.root.config(fg=fg)


# Класс для создания поля ввода (Entry)
class AppEntry:
    def __init__(self, root, font, width):
        # Создаем поле ввода
        self.root = tk.Entry(root, font=font, width=width)
        self.root.pack(pady=5)  # Позиционируем с отступами

    # Получить введённое значение
    def get(self):
        return self.root.get()

    # Очистить поле ввода
    def delete(self):
        return self.root.delete(0, tk.END)

class AppWindowModal:
    def __init__(self, parent, contact_data=None, on_save_callback=None, mode="edit", confirm_message=None, on_confirm=None):
        """
        :param parent: родительское окно (Toplevel)
        :param contact_data: словарь с данными контакта (включая ID)
        :param on_save_callback: функция, вызываемая после сохранения (например, обновление таблицы)
        """
        self.parent = parent
        self.contact_data = contact_data
        self.on_save_callback = on_save_callback
        self.mode = mode
        self.on_confirm = on_confirm
        self.entries = {}
        self.status_label = None
        self.create_window(confirm_message)

    def create_window(self, confirm_message):

        # Настраиваем окно
        self.parent.title("Редактировать контакт")
        self.parent.geometry("650x380")
        self.parent.resizable(False, False)
        self.parent.grab_set()  # Делает окно модальным
        self.parent.focus_set()

        if self.mode == "edit":
            fields = ["Имя", "Телефон", "Email", "Комментарий"]
            for field in fields:
                tk.Label(self.parent, text=f"{field}:", font=("Arial", 11)).pack(anchor="w", padx=20, pady=(10, 0))
                entry = tk.Entry(self.parent, width=50, font=("Arial", 10))
                entry.pack(padx=20, pady=5)
                entry.insert(0, self.contact_data.get(field, ""))
                self.entries[field] = entry

            # Статусная метка для сообщений
            self.status_label = tk.Label(self.parent, text="", font=("Arial", 10), fg="red")
            self.status_label.pack(pady=5)

            # Кнопка сохранения
            AppButton(
                self.parent,
                text="Сохранить",
                font=("Arial", 12),
                width=20,
                height=2,
                bg="green",
                fg="white",
                command=self.save_edits,
            )
        else:
            # Режим подтверждения
            AppLabel(
                self.parent,
                text=confirm_message or "Вы уверены, что хотите удалить контакт?")

            # Кнопка "Да"
            AppButton(
                self.parent,
                text="Да",
                font=("Arial", 12),
                width=10,
                height=2,
                bg="green",
                fg="white",
                command=self.confirm,
            )
            # Кнопка "Нет"
            AppButton(
                self.parent,
                text="Нет",
                font=("Arial", 12),
                width=10,
                height=2,
                bg="red",
                fg="white",
                command=self.parent.destroy,
            )


    def save_edits(self):
        """Сохраняет отредактированные данные контакта."""
        # Очищаем предыдущее сообщение
        self.status_label.config(text="")

        # Получаем данные из полей
        name = self.entries["Имя"].get().strip()
        phone = self.entries["Телефон"].get().strip()
        email = self.entries["Email"].get().strip()
        comment = self.entries["Комментарий"].get().strip()

        try:
            # Проверка обязательных полей
            if not name or not phone:
                raise EmptyFieldError("Имя и телефон обязательны!")

            if not is_valid_phone(phone):
                raise InvalidPhoneError("Телефон должен содержать минимум 10 цифр!")

            if email and not is_valid_email(email):
                raise InvalidEmailError("Неверный формат email!")

            # Обновляем данные контакта
            updated_contact = {
                "ID": self.contact_data["ID"],
                "Имя": name,
                "Телефон": phone,
                "Email": email,
                "Комментарий": comment
            }

            # Сохраняем изменения в файл (или БД)
            from model import update_contact
            update_contact(updated_contact)

            # Вызываем callback (обновить таблицу)
            if self.on_save_callback:
                self.on_save_callback()

            # Закрываем окно
            self.parent.destroy()

        except (EmptyFieldError, InvalidPhoneError, InvalidEmailError) as e:
            self.status_label.config(text=str(e))
        except Exception as e:
            self.status_label.config(text=f"Ошибка: {str(e)}")
            print("Неизвестная ошибка при сохранении:", e)
    def confirm(self):
        """Вызывается при нажатии 'Да' в режиме подтверждения"""
        if self.on_confirm:
            self.on_confirm()
        self.parent.destroy()

# --- Миксины для разделения функциональности ---

# Миксин для отображения стартового экрана
class StartScreenMixin:
    def show_start_screen(self):
        self.clear_screen()  # Очищаем окно

        # Список кнопок и соответствующих им функций
        buttons = [
            ("Показать все контакты", self.get_all_contacts),
            ("Создать контакт", self.create_contact),
            ("Найти контакт", self.search_contact),
            ("Изменить контакт", self.edit_contact),
            ("Выход", self.root.destroy),
        ]

        # Создаем кнопки
        for text, command in buttons:
            if text == "Выход":
                bg_color = "red"
            else:
                bg_color = "black"

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


# Миксин для отображения всех контактов
class ContactScreenMixin:
    def get_all_contacts(self):
        from Controller_dir.controller import get_all_contacts  # Чтобы избежать циклического импорта

        get_all_contacts(self.root, self)  # Передаем self (экземпляр App)


# Миксин для создания контакта
class CreateContactScreenMixin:
    def create_contact(self):
        from Controller_dir.controller import create_contact  # Чтобы избежать циклического импорта

        create_contact(self.root, self)  # Передаем self (экземпляр App)


# Миксин для поиска контакта
class SearchContactScreenMixin:
    def search_contact(self):
        from Controller_dir.controller import search_contact  # Чтобы избежать циклического импорта

        search_contact(self.root, self)  # Передаем self (экземпляр App)


# Миксин для редактирования контакта
class EditContactScreenMixin:
    def edit_contact(self):
        from Controller_dir.controller import edit_contact  # Чтобы избежать циклического импорта
        edit_contact(self.root, self)  # Передаем self (экземпляр App)


# --- Основной класс приложения ---

# Главный класс приложения, использующий миксины для расширения функциональности
class App(
    StartScreenMixin,
    ContactScreenMixin,
    CreateContactScreenMixin,
    SearchContactScreenMixin,
    EditContactScreenMixin):
    def __init__(self, root):
        # Инициализируем главное окно
        self.root = root
        self.root.title("Телефонный справочник")
        self.root.geometry("1000x850")  # Размер окна
        self.root.configure(bg="black")  # Фон окна
        self.show_start_screen()  # Показываем стартовый экран

    # Метод для очистки окна от всех виджетов
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()