from typing import Iterable, Iterator, Generator
from src.task import Task, TaskStatus


class TaskQueueIterator(Iterator[Task]):
    def __init__(self, tasks: list):
        self._tasks = tasks
        self._index = 0

    def __iter__(self) -> "TaskQueueIterator":
        return self

    def __next__(self) -> Task:
        if self._index >= len(self._tasks):
            raise StopIteration

        task = self._tasks[self._index]
        self._index += 1
        return task


class TaskQueue(Iterable[Task]):
    def __init__(self, tasks: Iterable[Task] | None = None):
        self._tasks = list(tasks) if tasks else []

    def add_task(self, task: Task) -> None:
        self._tasks.append(task)

    def extend_tasks(self, tasks: Iterable[Task]) -> None:
        self._tasks.extend(tasks)

    def __iter__(self) -> TaskQueueIterator:
        return TaskQueueIterator(self._tasks)

    def __len__(self):
        return len(self._tasks)

    def filter_by_status(self, status: TaskStatus) -> Generator[Task, None, None]:
        for task in self._tasks:
            if task.status == status:
                yield task

    def filter_by_priority(self, priority: int) -> Generator[Task, None, None]:
        for task in self._tasks:
            if task.priority == priority:
                yield task

    def get_ready_tasks(self) -> Generator[Task, None, None]:
        for task in self._tasks:
            if task.ready_for_execution:
                yield task
