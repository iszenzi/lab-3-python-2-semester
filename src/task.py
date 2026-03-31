from dataclasses import dataclass
from typing import Any
from exceptions import InvalidPriorityError


class Task:
    """
    Модель задачи
    :param id: Идентификатор задачи
    :param payload: Данные задачи
    """

    def __init__(self, id: int, payload: Any, priority: int, descriptons: str = ""):
        self.id = id
        self.payload = payload
        self.priority = priority
        self.descriptons = descriptons

    @property
    def id(self) -> int:
        return self._id
