import tkinter as tk
from tkinter import ttk
import csv
import uuid

# Объявление глобальных переменных для полей ввода и метки статуса
global entry_name, entry_phone, entry_email, entry_comment, status_label, selected_contact_id


# Функция загрузки контактов из файла CSV
def load_contacts():
    with open("Контакты.txt", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        content = list(reader)
        return content


# Функция записи контактов в файл CSV
def write_contacts(contacts, filename="Контакты.txt"):
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


def destroy_widget():
    # Очистка окна
    for widget in window.winfo_children():
        widget.destroy()


def treeview():

    # Создание таблицы
    columns = ("ID", "Имя", "Телефон", "Email", "Комментарий")
    tree = ttk.Treeview(window, columns=columns, show="headings")
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)

        # Чтение данных из файла
        contacts = load_contacts()

        # Добавление данных в таблицу
        for contact in contacts:
            tree.insert(
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
    return tree


# Функция отображения начального экрана
def show_start_screen():

    destroy_widget()

    # Добавляем кнопку "Показать все контакты"
    btn_get_all_contacts = tk.Button(
        window,
        text="Показать все контакты",
        font=("Courier New", 15, "bold"),
        width=45,
        height=4,
        bg="black",
        fg="white",
        command=get_all_contacts,
    )
    btn_get_all_contacts.pack(expand=True, fill=tk.BOTH)

    # Добавляем кнопку "Создать контакт"
    btn_create = tk.Button(
        window,
        text="Создать контакт",
        font=("Courier New", 15, "bold"),
        width=45,
        height=4,
        bg="black",
        fg="white",
        command=create_contact,
    )
    btn_create.pack(expand=True, fill=tk.BOTH)

    # Добавляем кнопку "Найти контакт"
    btn_search = tk.Button(
        window,
        text="Найти контакт",
        font=("Courier New", 15, "bold"),
        width=45,
        height=4,
        bg="black",
        fg="white",
        command=search_contact,
    )
    btn_search.pack(expand=True, fill=tk.BOTH)

    # Добавляем кнопку "Изменить контакт"
    btn_edit = tk.Button(
        window,
        text="Изменить контакт",
        font=("Courier New", 15, "bold"),
        width=45,
        height=4,
        bg="black",
        fg="white",
        command=edit_contact,
    )
    btn_edit.pack(expand=True, fill=tk.BOTH)

    # Добавляем кнопку "Выход"
    btn_exit = tk.Button(
        window,
        text="Выход",
        font=("Courier New", 13, "bold"),
        width=45,
        height=4,
        command=window.destroy,
    )
    btn_exit.pack(pady=20)


# Функция отображения всех контактов
def get_all_contacts():
    destroy_widget()
    treeview()

    # Кнопка назад
    back_button = tk.Button(
        window,
        text="Назад",
        font=("Arial", 12),
        width=15,
        height=2,
        command=show_start_screen,
    )
    back_button.pack(pady=10)


def is_valid_phone(phone):
    return phone.isdigit() and len(phone) >= 10


# Функция для проверки email
def is_valid_email(email):
    return "@" in email and "." in email


# Функция создания нового контакта
def create_contact():

    destroy_widget()

    def save_new_contact():
        # Получаем данные из полей ввода
        name = entry_name.get()
        phone = entry_phone.get()
        email = entry_email.get()
        comment: str = entry_comment.get()

        # Добавлено в класс Contact
        # Проверяем обязательные поля: имя и телефон не должны быть пустыми
        if not name.strip() or not phone.strip():
            # Если одно из полей пустое — выводим сообщение об ошибке
            status_label.config(text="Имя и телефон обязательны!", fg="red")
            return

        if not is_valid_phone(phone):
            status_label.config(
                text="Телефон должен содержать минимум 10 цифр!", fg="red"
            )
            return

        if email and not is_valid_email(
            email
        ):  # email необязательный, поэтому проверяем только если заполнен
            status_label.config(
                text="Неверный формат email (пример: user@example.com)", fg="red"
            )
            return

        # Открываем CSV-файл на дозапись и записываем данные нового контакта
        new_contact = add_contact(name=name, phone=phone, email=email, comment=comment)

        # Очищаем все поля ввода после успешного сохранения
        entry_name.delete(0, tk.END)
        entry_phone.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        entry_comment.delete(0, tk.END)

        # Выводим статусное сообщение об успешном сохранении
        status_label.config(text="Данные сохранены!", fg="green")

    # Создание метки и поля ввода для Имени
    label_name = tk.Label(window, text="Имя:")
    label_name.pack(anchor="c", padx=10)
    entry_name = tk.Entry(window, width=80)  # Поле ввода имени
    entry_name.pack(padx=10, pady=5)

    # Создание метки и поля ввода для Телефона
    label_phone = tk.Label(window, text="Телефон:")
    label_phone.pack(anchor="c", padx=10)
    entry_phone = tk.Entry(window, width=80)
    entry_phone.pack(padx=10, pady=5)

    # Создание метки и поля ввода для Email
    label_email = tk.Label(window, text="Email:")
    label_email.pack(anchor="c", padx=10)
    entry_email = tk.Entry(window, width=80)
    entry_email.pack(padx=10, pady=5)

    # Создание метки и поля ввода для Комментария
    label_comment = tk.Label(window, text="Комментарий:")
    label_comment.pack(anchor="c", padx=10)
    entry_comment = tk.Entry(window, width=80)
    entry_comment.pack(padx=10, pady=5)

    # Метка для отображения статуса операции (ошибка или успех)
    status_label = tk.Label(window, text="", font=("Arial", 10), fg="black")
    status_label.pack(pady=5)

    # Кнопка для сохранения нового контакта
    button_save_new_contact = tk.Button(
        window,
        text="Сохранить",
        font=("Arial", 12),
        width=15,
        height=2,
        command=save_new_contact,
    )
    button_save_new_contact.pack(pady=10)

    # Кнопка для возврата на главный экран
    back_button = tk.Button(
        window,
        text="Назад",
        font=("Arial", 12),
        width=15,
        height=2,
        command=show_start_screen,
    )
    back_button.pack(pady=10)


# Функция поиска контактов
def search_contact():

    destroy_widget()

    # Поля ввода для поиска
    tk.Label(window, text="Имя:").pack(anchor="w", padx=10)
    entry_name = tk.Entry(window, width=40)
    entry_name.pack(padx=10, pady=5)

    tk.Label(window, text="Телефон:").pack(anchor="w", padx=10)
    entry_phone = tk.Entry(window, width=40)
    entry_phone.pack(padx=10, pady=5)

    tk.Label(window, text="Email:").pack(anchor="w", padx=10)
    entry_email = tk.Entry(window, width=40)
    entry_email.pack(padx=10, pady=5)

    tk.Label(window, text="Комментарий:").pack(anchor="w", padx=10)
    entry_comment = tk.Entry(window, width=40)
    entry_comment.pack(padx=10, pady=5)

    columns = ("ID", "Имя", "Телефон", "Email", "Комментарий")
    tree = ttk.Treeview(window, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def perform_search():
        # Удаляем текущие строки из таблицы
        for row in tree.get_children():
            tree.delete(row)

        # Считываем данные из полей
        name = entry_name.get().strip().lower()
        phone = entry_phone.get().strip().lower()
        email = entry_email.get().strip().lower()
        comment = entry_comment.get().strip().lower()

        contacts = load_contacts()
        results = []

        for contact in contacts:
            match = True
            if name and name not in contact["Имя"].lower():
                match = False
            if phone and phone not in contact["Телефон"].lower():
                match = False
            if email and email not in contact["Email"].lower():
                match = False
            if comment and comment not in contact.get("Комментарий", "").lower():
                match = False
            if match:
                results.append(contact)

        # Добавляем найденные результаты в таблицу
        for contact in results:
            tree.insert(
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

    # Кнопка поиска
    search_button = tk.Button(
        window,
        text="Найти",
        font=("Arial", 12),
        width=15,
        height=2,
        command=perform_search,
    )
    search_button.pack(pady=10)

    # Кнопка для возврата на главный экран
    back_button = tk.Button(
        window,
        text="Назад",
        font=("Arial", 12),
        width=15,
        height=2,
        command=show_start_screen,
    )
    back_button.pack(pady=10)


def edit_contact():

    destroy_widget()
    tree = treeview()

    def refresh_table():
        contacts = load_contacts()
        for row in tree.get_children():
            tree.delete(row)
        for contact in contacts:
            tree.insert(
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
        update_button_states()

    def update_button_states():
        selected_items = tree.selection()
        edit_button.config(state=tk.NORMAL if selected_items else tk.DISABLED)
        delete_button.config(state=tk.NORMAL if selected_items else tk.DISABLED)

    def on_select(event):
        global selected_contact_id
        selected_items = tree.selection()
        if not selected_items:
            # Ничего не выбрано, можно обнулить ID или выйти
            selected_contact_id = None
            update_button_states()
            return
        selected_item = selected_items[0]
        values = tree.item(selected_item)["values"]
        selected_contact_id = values[0]  # Теперь это id
        update_button_states()

    def open_edit_window():
        # Получаем идентификатор выбранной строки
        selected_items = tree.selection()
        # Получаем значения из выбранной строки
        selected_item = selected_items[0]
        values = tree.item(selected_item)["values"]
        contact_data = {
            "ID": values[0],
            "Имя": values[1],
            "Телефон": values[2],
            "Email": values[3],
            "Комментарий": values[4],
        }

        def save_edits():
            edited_contact = {
                "ID": selected_contact_id,
                "Имя": entries["Имя"].get(),
                "Телефон": entries["Телефон"].get(),
                "Email": entries["Email"].get(),
                "Комментарий": entries["Комментарий"].get(),
            }

            # Проверяем обязательные поля: имя и телефон не должны быть пустыми
            if not edited_contact["Имя"] or not edited_contact["Телефон"]:
                # Если одно из полей пустое — выводим сообщение об ошибке
                status_label.config(text="Имя и телефон обязательны!", fg="red")
                return

            if not is_valid_phone(edited_contact["Телефон"]):
                status_label.config(
                    text="Телефон должен содержать минимум 10 цифр!", fg="red"
                )
                return

            if edited_contact["Email"] and not is_valid_email(
                edited_contact["Email"]
            ):  # email необязательный, поэтому проверяем только если заполнен
                status_label.config(
                    text="Неверный формат email (пример: user@example.com)", fg="red"
                )
                return

            contacts = load_contacts()
            for i, c in enumerate(contacts):
                if c["ID"] == selected_contact_id:
                    contacts[i] = edited_contact  # Заменяем контакт
                    break
            write_contacts(contacts)
            refresh_table()
            edit_win.destroy()

        # Создаем окно редактирования
        edit_win = tk.Toplevel(window)
        edit_win.title("Редактировать контакт")
        edit_win.geometry("400x300")

        entries = {}
        fields = ["Имя", "Телефон", "Email", "Комментарий"]
        for field in fields:
            tk.Label(edit_win, text=field).pack(anchor=tk.W, padx=10)
            entry = tk.Entry(edit_win, width=40)
            entry.pack(padx=10, pady=5)
            entry.insert(0, contact_data[field])
            entries[field] = entry

        save_edit_btn = tk.Button(
            edit_win, text="Сохранить изменения", command=save_edits
        )
        save_edit_btn.pack(padx=10)

        # Метка для отображения статуса (ошибок или успеха)
        status_label = tk.Label(edit_win, text="", font=("Arial", 10), fg="red")
        status_label.pack(pady=5)

    def delete_contact():
        # Получаем идентификатор выбранной строки
        selected_item = tree.selection()[0]
        # Получаем значения из выбранной строки
        values = tree.item(selected_item)["values"]
        contact_id_delete = values[0]
        contacts = load_contacts()
        contacts = [
            contact for contact in contacts if contact["ID"] != contact_id_delete
        ]
        write_contacts(contacts)

    # Событие выделения строки
    tree.bind("<<TreeviewSelect>>", on_select)

    # Кнопка редактировать
    edit_button = tk.Button(
        window,
        text="Редактировать",
        font=("Arial", 12),
        state=tk.DISABLED,
        width=15,
        height=2,
        command=open_edit_window,
    )
    edit_button.pack(pady=10)

    # Кнопка удалить
    delete_button = tk.Button(
        window,
        text="Удалить",
        font=("Arial", 12),
        state=tk.DISABLED,
        width=15,
        height=2,
        command=delete_contact,
    )
    delete_button.pack(pady=10)

    # Кнопка назад
    back_button = tk.Button(
        window,
        text="Назад",
        font=("Arial", 12),
        width=15,
        height=2,
        command=show_start_screen,
    )
    back_button.pack(pady=10)


# Создание главного окна
window = tk.Tk()
window.title("Телефонный справочник")
window.geometry("900x850")

# Показываем начальный экран
show_start_screen()

# Установка цвета фона окна
window.configure(bg="black")

# Запуск главного цикла
window.mainloop()
