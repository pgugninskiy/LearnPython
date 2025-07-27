class ContactError(Exception):
    """Базовый класс для ошибок, связанных с контактами"""
    pass

class EmptyFieldError(ContactError):
    def __init__(self, message="Имя и телефон обязательны для заполнения."):
        super().__init__(message)

class InvalidPhoneError(ContactError):
    def __init__(self, message="Телефон должен содержать минимум 10 цифр."):
        super().__init__(message)

class InvalidEmailError(ContactError):
    def __init__(self, message="Неверный формат email (пример: user@example.com)."):
        super().__init__(message)
