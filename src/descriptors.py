from typing import Any
from exceptions import InvalidPriorityError


class PriorityDescriptor:
    """
    Дескриптор данных для валидации приоритета задачи.
    """

    def __init__(self, min_val: int = 1, max_val: int = 5):
        self.min_val = min_val
        self.max_val = max_val

    def __set_name__(self, owner: type, name: str) -> None:
        self.public_name = name
        self.private_name = f"_{name}"

    def __get__(self, instance: Any, owner: type) -> Any:
        if instance is None:
            return self
        return getattr(instance, self.private_name)

    def __set__(self, instance: Any, value: int) -> None:
        if not isinstance(value, int):
            raise InvalidPriorityError(
                f"Приоритет должен быть целым числом, получено: {type(value).__name__}"
            )

        if not (self.min_val <= value <= self.max_val):
            raise InvalidPriorityError(
                f"Приоритет должен быть в диапазоне от {self.min_val} до {self.max_val}. "
                f"Получено: {value}"
            )

        setattr(instance, self.private_name, value)
