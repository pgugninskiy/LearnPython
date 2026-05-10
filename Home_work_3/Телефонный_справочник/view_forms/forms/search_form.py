from typing import Callable, Optional
from tkinter import Tk
from view_forms.view import AppLabel, AppEntry, AppButton


class SearchContactForm:
    """
    Форма для поиска контактов.
    Отвечает только за UI и сбор критериев поиска.
    Поиск делегируется внешней функции (callback).
    """

    def __init__(
        self,
        parent: Tk,
        on_search: Callable[[str, str, str, str], None],
        on_cancel: Callable[[], None],
    ) -> None:
        self.parent = parent
        self.on_search = on_search
        self.on_cancel = on_cancel

        self._build_ui()

    def _build_ui(self) -> None:
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
            text="Поиск",
            font=("Arial", 12),
            width=15,
            height=2,
            bg="blue",
            fg="white",
            command=self._on_search_click,
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

    def _on_search_click(self) -> None:
        """Собирает критерии и вызывает callback."""
        name = self.entry_name.get().strip()
        phone = self.entry_phone.get().strip()
        email = self.entry_email.get().strip()
        comment = self.entry_comment.get().strip()

        self.on_search(name, phone, email, comment)