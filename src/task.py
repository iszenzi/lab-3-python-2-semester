from typing import Any
from enum import Enum
from datetime import datetime
from src.exceptions import InvalidStateError
from src.descriptors import PriorityDescriptor, DefaultDescriptionDescriptor


class TaskStatus(Enum):
    """Статусы задачи"""

    NEW = "new"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class Task:
    """
    Модель задачи
    """

    priority = PriorityDescriptor(min_val=1, max_val=5)
    description = DefaultDescriptionDescriptor()

    def __init__(
        self, id: int, payload: Any, priority: int = 3, description: str = ""
    ) -> None:
        """
        Инициализирует новую задачу
        :param id: Идентификатор задачи
        :param payload: Полезная нагрузка задачи
        :param priority: Приоритет задачи
        :param description: Описание задачи
        """
        self._id = id
        self.payload = payload
        self.priority = priority
        self._status = TaskStatus.NEW
        self._created_at = datetime.now()

        if description:
            self.description = description

    @property
    def id(self) -> int:
        """
        Возвращает идентификатор задачи
        :return: Идентификатор задачи
        """
        return self._id

    @property
    def created_at(self) -> datetime:
        """
        Возвращает время создания задачи
        :return: Отметка времени
        """
        return self._created_at

    @property
    def status(self) -> TaskStatus:
        """
        Возвращает текущий статус задачи
        :return: Статус задачи
        """
        return self._status

    @property
    def ready_for_execution(self) -> bool:
        """
        Проверяет, готова ли задача к выполнению
        :return: True, если статус задачи NEW, иначе False
        """
        return self.status == TaskStatus.NEW

    def start(self) -> None:
        """
        Переводит задачу в статус IN_PROGRESS
        """
        if self._status != TaskStatus.NEW:
            raise InvalidStateError(
                f"Нельзя запустить задачу в статусе {self._status.value}"
            )
        self._status = TaskStatus.IN_PROGRESS

    def complete(self) -> None:
        """
        Переводит задачу в статус COMPLETED
        """
        if self._status != TaskStatus.IN_PROGRESS:
            raise InvalidStateError("Завершить можно только начатую задачу")
        self._status = TaskStatus.COMPLETED

    def fail(self) -> None:
        """
        Переводит задачу в статус FAILED
        """
        if self._status not in (TaskStatus.IN_PROGRESS, TaskStatus.NEW):
            raise InvalidStateError(
                "Завершить с ошибкой можно только начатую или новую задачу"
            )
        self._status = TaskStatus.FAILED

    def __repr__(self):
        """
        Возвращает строковое представление задачи
        :return: Строка с представлением
        """
        return (
            f"Task(id={self.id}, priority={self.priority}, status={self.status.value})"
        )
