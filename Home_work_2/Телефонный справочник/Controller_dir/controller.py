from model import (
    load_contacts,
    write_contacts,
    add_contact,
    delete_contact,
    is_valid_phone,
    is_valid_email,
)
from view import AppButton, AppTable, AppLabel, AppEntry, AppWindowModal
from .exceptions import *
import tkinter as tk


def get_all_contacts(root, App):
    # Очистка экрана перед отображением списка контактов
    App.clear_screen()
    # Определение заголовков колонок таблицы
    columns = ("ID", "Имя", "Телефон", "Email", "Комментарий")
    # Создание экземпляра таблицы (AppTable) для отображения контактов
    tree = AppTable(root, columns=columns, show="headings", height=800)
    # Скрываем колонку ID, но оставляем её в данных
    tree.table.column("ID", width=0, stretch=tk.NO)  # Полностью скрываем
    tree.table.heading("ID", text="ID")
    # Загрузка всех контактов из хранилища (например, файла или БД)
    contacts = load_contacts()
    # Добавление данных контактов в таблицу
    tree.load_contact(contacts)

    # Кнопка "Назад" — возвращает на стартовый экран приложения
    AppButton(
        root,
        text="Назад",
        font=("Arial", 12),
        width=15,  # ширина кнопки
        height=2,  # высота кнопки
        bg="red",
        fg="white",
        command=App.show_start_screen,  # переход обратно на начальный экран
    )


def create_contact(root, App):
    # Очистка экрана перед отображением списка контактов
    App.clear_screen()

    # Создаем экземпляр AppLabel для статусных сообщений, изначально пустой
    status_label_instance = AppLabel(root, text="")
    status_label_instance.clear_status()

    # Создание экземпляра метки (AppLabel) для указания имени поля ввода
    AppLabel(root, text="Имя:")
    entry_name = AppEntry(root, ("Arial", 12), 80)

    AppLabel(root, text="Телефон:")
    entry_phone = AppEntry(root, ("Arial", 12), 80)

    AppLabel(root, text="Email")
    entry_email = AppEntry(root, ("Arial", 12), 80)

    AppLabel(root, text="Комментарий")
    entry_comment = AppEntry(root, ("Arial", 12), 80)

    def save_new_contact():

        status_label_instance.clear_status()
        # Получаем данные из полей ввода
        name = entry_name.get().strip()
        phone = entry_phone.get().strip()
        email = entry_email.get().strip()
        comment = entry_comment.get().strip()

        try:

            # Проверяем обязательные поля: имя и телефон не должны быть пустыми
            if not name.strip() or not phone.strip():
                raise EmptyFieldError()

            if not is_valid_phone(phone):
                raise InvalidPhoneError()

            if email and not is_valid_email(email):
                # email необязательный, поэтому проверяем только если заполнен
                raise InvalidEmailError()

            add_contact(name=name, phone=phone, email=email, comment=comment)

            # Очищаем все поля ввода после успешного сохранения
            entry_name.delete()
            entry_phone.delete()
            entry_email.delete()
            entry_comment.delete()

            # Выводим статусное сообщение об успешном сохранении
            status_label_instance.update_text("Данные сохранены!", fg="green")

        except (EmptyFieldError, InvalidPhoneError, InvalidEmailError) as e:
            status_label_instance.update_text(str(e), fg="red")
        except Exception as e:
            status_label_instance.update_text(f"Произошла ошибка: {str(e)}", fg="red")
            print("Неизвестная ошибка:", e)

    # Кнопка "Сохранить" — выполняет сохранение данных нового контакта
    AppButton(
        root,
        text="Сохранить",
        font=("Arial", 12),
        width=15,  # ширина кнопки
        height=2,  # высота кнопки
        bg="black",
        fg="white",
        command=save_new_contact,  # переход обратно на начальный экран
    )

    # Кнопка "Назад" — возвращает на стартовый экран приложения
    AppButton(
        root,
        text="Назад",
        font=("Arial", 12),
        width=15,  # ширина кнопки
        height=2,  # высота кнопки
        bg="red",
        fg="white",
        command=App.show_start_screen,  # переход обратно на начальный экран
    )


def search_contact(root, App):
    # Очистка экрана перед отображением списка контактов
    App.clear_screen()

    # Определение заголовков колонок таблицы
    columns = ("ID", "Имя", "Телефон", "Email", "Комментарий")

    # Создание экземпляра таблицы (AppTable) для отображения контактов
    tree = AppTable(root, columns=columns, show="headings", height=450)
    # Скрываем колонку ID, но оставляем её в данных
    tree.table.column("ID", width=0, stretch=tk.NO)  # Полностью скрываем
    tree.table.heading("ID", text="ID")

    # Загрузка всех контактов из хранилища (например, файла или БД)
    contacts = load_contacts()

    # Добавление данных контактов в таблицу
    tree.load_contact(contacts)

    def perform_search():
        for item in tree.table.get_children():
            tree.table.delete(item)

        name_query = entry_name.get().strip().lower()
        phone_query = entry_phone.get().strip().lower()
        email_query = entry_email.get().strip().lower()
        comment_query = entry_comment.get().strip().lower()

        results = []
        for contact in contacts:
            match = True
            if name_query and name_query not in contact["Имя"].lower():
                match = False
            if phone_query and phone_query not in contact["Телефон"].lower():
                match = False
            if email_query and email_query not in contact["Email"].lower():
                match = False
            if (
                comment_query
                and comment_query not in contact.get("Комментарий", "").lower()
            ):
                match = False
            if match:
                results.append(contact)

        # Добавление данных контактов в таблицу
        tree.load_contact(results)

    # Создание экземпляра метки (AppLabel) для указания имени поля ввода
    AppLabel(root, text="Имя:")
    entry_name = AppEntry(root, ("Arial", 12), 80)

    # Создание экземпляра метки (AppLabel) для указания телефона поля ввода
    AppLabel(root, text="Телефон:")
    entry_phone = AppEntry(root, ("Arial", 12), 80)

    # Создание экземпляра метки (AppLabel) для указания Email поля ввода
    AppLabel(root, text="Email")
    entry_email = AppEntry(root, ("Arial", 12), 80)

    # Создание экземпляра метки (AppLabel) для указания Комментарий поля ввода
    AppLabel(root, text="Комментарий")
    entry_comment = AppEntry(root, ("Arial", 12), 80)

    # Кнопка "Поиск"
    AppButton(
        root,
        text="Поиск",
        font=("Arial", 12),
        width=15,  # ширина кнопки
        height=2,  # высота кнопки
        bg="blue",
        fg="white",
        command=perform_search,
    )

    # Кнопка "Назад" — возвращает на стартовый экран приложения
    AppButton(
        root,
        text="Назад",
        font=("Arial", 12),
        width=15,  # ширина кнопки
        height=2,  # высота кнопки
        bg="red",
        fg="white",
        command=App.show_start_screen,  # переход обратно на начальный экран
    )


def edit_contact(root, App):
    # Очистка экрана перед отображением списка контактов
    App.clear_screen()

    # Определение заголовков колонок таблицы
    columns = ("ID", "Имя", "Телефон", "Email", "Комментарий")

    # Создание экземпляра таблицы (AppTable) для отображения контактов
    tree = AppTable(root, columns=columns, show="headings", height=450)
    # Скрываем колонку ID, но оставляем её в данных
    tree.table.column("ID", width=0, stretch=tk.NO)  # Полностью скрываем
    tree.table.heading("ID", text="ID")

    # Загрузка всех контактов из хранилища (например, файла или БД)
    contacts = load_contacts()

    # Добавление данных контактов в таблицу
    tree.load_contact(contacts)

    # Создаем экземпляр AppLabel для статусных сообщений, изначально пустой
    status_label_instance = AppLabel(root, text="")

    def open_edit_window():

        selected_items = tree.selection()
        if not selected_items:
            status_label_instance.update_text(
                text="Выберите контакт для редактирования!", fg="red"
            )
            return

        selected_item = selected_items[0]
        values = tree.item(selected_item)["values"]
        contact_id = values[0]  # Теперь ID доступен

        contact_data = next((c for c in contacts if c["ID"] == contact_id), None)

        if not contact_data:
            status_label_instance.update_text(text="Контакт не найден!", fg="red")
            return

        def on_contact_saved():
            # Обновляем таблицу
            tree.refresh_table(load_contacts)
            # Отображаем сообщение об успехе на основном экране
            status_label_instance.update_text(text="Данные успешно изменены!", fg="green")

        # Создаём окно редактирования
        edit_win = tk.Toplevel(root)
        AppWindowModal(
            parent=edit_win,
            contact_data=contact_data,
            on_save_callback=on_contact_saved,
        )

    def confirm_delete():

        selected_items = tree.selection()

        if not selected_items:
            status_label_instance.update_text(
                text="Выберите контакт для удаления!", fg="red"
            )
            return

        selected_item = selected_items[0]
        values = tree.item(selected_item)["values"]
        contact_id = values[0]
        contact_name = values[1]

        def do_delete():
            success = delete_contact(contact_id)
            if success:
                status_label_instance.update_text(
                    text=f"Контакт '{contact_name}' удалён!", fg="green"
                )
                tree.refresh_table(load_contacts)
            else:
                status_label_instance.update_text(text="Контакт не найден!", fg="red")

        # Открываем модальное окно подтверждения
        confirm_win = tk.Toplevel(root)
        AppWindowModal(
            parent=confirm_win,
            mode="confirm",
            confirm_message=f"Вы действительно хотите удалить контакт:\n'{contact_name}'?",
            on_confirm=do_delete,
        )

    # Кнопка "Изменить" — возвращает на стартовый экран приложения
    AppButton(
        root,
        text="Изменить",
        font=("Arial", 12),
        width=15,  # ширина кнопки
        height=2,  # высота кнопки
        bg="black",
        fg="white",
        command=open_edit_window,  # переход обратно на начальный экран
    )

    # Кнопка "Удалить" — возвращает на стартовый экран приложения
    AppButton(
        root,
        text="Удалить",
        font=("Arial", 12),
        width=15,  # ширина кнопки
        height=2,  # высота кнопки
        bg="black",
        fg="white",
        command=confirm_delete,
    )

    # Кнопка "Назад" — возвращает на стартовый экран приложения
    AppButton(
        root,
        text="Назад",
        font=("Arial", 12),
        width=15,  # ширина кнопки
        height=2,  # высота кнопки
        bg="red",
        fg="white",
        command=App.show_start_screen,  # переход обратно на начальный экран
    )