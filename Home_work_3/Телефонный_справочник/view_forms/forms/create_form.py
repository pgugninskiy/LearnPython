from typing import Callable, Optional
from tkinter import Tk
from view_forms.view import AppLabel, AppEntry, AppButton  # импортируем твои UI-компоненты


class CreateContactForm :
    """
    Форма для создания нового контакта.
    Отвечает только за UI и сбор данных.
    Сохранение делегируется внешней функции (callback).
    """
    def __init__(self,
        parent: Tk,
        on_save: Callable[[str, str, str, str], None],
        on_cancel: Callable[[], None], ) -> None:
        """
                :param parent: родительское окно (обычно root)
                :param on_save: функция, вызываемая при успешном сохранении.
                                Принимает (name, phone, email, comment).
                :param on_cancel: функция, вызываемая при нажатии "Назад".
                """
        self.parent = parent
        self.on_save = on_save
        self.on_cancel = on_cancel
        self.status_label: Optional[AppLabel] = None

        self._build_ui()

    def _build_ui(self) -> None:
        """Создаёт все элементы интерфейса."""

        # Поля ввода
        AppLabel(self.parent, text="Имя:")
        self.entry_name = AppEntry(self.parent, ("Arial", 12), 80)

        AppLabel(self.parent, text="Телефон:")
        self.entry_phone = AppEntry(self.parent, ("Arial", 12), 80)

        AppLabel(self.parent, text="Email:")
        self.entry_email = AppEntry(self.parent, ("Arial", 12), 80)

        AppLabel(self.parent, text="Комментарий:")
        self.entry_comment = AppEntry(self.parent, ("Arial", 12), 80)

        # Кнопки
        AppButton(
            self.parent,
            text="Сохранить",
            font=("Arial", 12),
            width=15,
            height=2,
            bg="black",
            fg="white",
            command=self._on_save_click,
        )
        AppButton(
            self.parent,
            text="Назад",
            font=("Arial", 12),
            width=15,
            height=2,
            bg="red",
            fg="white",
            command=self.on_cancel,
        )

    def _clear_status(self) -> None:
        """Удаляет предыдущее сообщение об ошибке/успехе."""
        if self.status_label:
            self.status_label.destroy()
            self.status_label = None

    def _on_save_click(self) -> None:
        """Обрабатывает нажатие кнопки 'Сохранить'."""
        self._clear_status()

        name = self.entry_name.get().strip()
        phone = self.entry_phone.get().strip()
        email = self.entry_email.get().strip()
        comment = self.entry_comment.get().strip()

        # Передаём данные наружу — контроллер сам решит, что с ними делать
        self.on_save(name, phone, email, comment)

    def show_message(self, text: str, color: str = "red") -> None:
        """Показывает сообщение под формой (например, об ошибке)."""
        self._clear_status()
        self.status_label = AppLabel(self.parent, text=text, fg=color)