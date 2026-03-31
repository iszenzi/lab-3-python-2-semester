from typing import Any
from enum import Enum
from datetime import datetime
from exceptions import InvalidStateError
from descriptors import PriorityDescriptor, DefaultDescriptionDescriptor


class TaskStatus(Enum):
    """Статусы задачи"""

    NEW = "new"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class Task:
    priority = PriorityDescriptor(min_val=1, max_val=5)
    description = DefaultDescriptionDescriptor()

    def __init__(
        self, id: int, payload: Any, priority: int, description: str = ""
    ) -> None:
        self._id = id
        self.payload = payload
        self.priority = priority
        self._status = TaskStatus.NEW
        self._created_at = datetime.now()

        if description:
            self.description = description

    @property
    def id(self) -> int:
        return self._id

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def status(self) -> TaskStatus:
        return self._status

    @property
    def ready_for_execution(self) -> bool:
        return self.status == TaskStatus.NEW

    def start(self) -> None:
        if self._status != TaskStatus.NEW:
            raise InvalidStateError(
                f"Нельзя запустить задачу в статусе {self._status.value}"
            )
        self._status = TaskStatus.IN_PROGRESS

    def complete(self) -> None:
        if self._status != TaskStatus.IN_PROGRESS:
            raise InvalidStateError("Завершить можно только начатую задачу")
        self._status = TaskStatus.COMPLETED

    def fail(self) -> None:
        if self._status not in (TaskStatus.IN_PROGRESS, TaskStatus.NEW):
            raise InvalidStateError("Завершить можно только начатую задачу")
        self._status = TaskStatus.FAILED

    def __repr__(self):
        return (
            f"Task(id={self.id}, priority={self.priority}, status={self.status.value})"
        )
