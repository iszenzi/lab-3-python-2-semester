import logging
from typing import Iterable, Iterator, Generator
from src.task import Task, TaskStatus


class TaskQueueIterator(Iterator[Task]):
    """
    Итератор для последовательного обхода задач в очереди
    """

    def __init__(self, tasks: list[Task]) -> None:
        """
        Инициализирует итератор очереди задач
        :param tasks: Список задач для обхода
        """
        self._tasks = tasks
        self._index = 0

    def __iter__(self) -> "TaskQueueIterator":
        """
        Возвращает сам итератор
        :return: Текущий экземпляр TaskQueueIterator
        """
        return self

    def __next__(self) -> Task:
        """
        Возвращает следующую задачу в очереди
        :return: Объект задачи
        """
        if self._index >= len(self._tasks):
            raise StopIteration

        task = self._tasks[self._index]
        self._index += 1
        return task


class TaskQueue(Iterable[Task]):
    """
    Ленивая очередь задач с поддержкой генераторов и многократного итерирования
    """

    def __init__(self, tasks: Iterable[Task] | None = None) -> None:
        """
        Инициализирует очередь задач
        :param tasks: Коллекция задач для начального заполнения очереди
        """
        self._tasks: list[Task] = list(tasks) if tasks else []
        logging.info(f"Создана очередь задач (элементов: {len(self._tasks)})")

    def add_task(self, task: Task) -> None:
        """
        Добавляет одну задачу в конец очереди
        :param task: Объект добавляемой задачи
        """
        self._tasks.append(task)
        logging.info(f"Задача #{task.id} добавлена в очередь")

    def extend_tasks(self, tasks: Iterable[Task]) -> None:
        """
        Расширяет очередь переданным набором задач
        :param tasks: Коллекция задач для добавления
        """
        tasks_list = list(tasks)
        self._tasks.extend(tasks_list)
        logging.info(f"Добавлено {len(tasks_list)} задач в очередь")

        self._tasks.extend(tasks)

    def __iter__(self) -> TaskQueueIterator:
        """
        Возвращает новый итератор для многократного обхода
        :return: Новый экземпляр TaskQueueIterator
        """
        return TaskQueueIterator(self._tasks)

    def __len__(self) -> int:
        """
        Возвращает текущее количество задач в очереди
        :return: Количество задач
        """
        return len(self._tasks)

    def filter_by_status(self, status: TaskStatus) -> Generator[Task, None, None]:
        """
        Генератор для ленивой фильтрации по статусу задачи
        :param status: Искомый статус задачи
        :return: Генератор задач с указанным статусом
        """
        for task in self._tasks:
            if task.status == status:
                yield task

    def filter_by_priority(self, priority: int) -> Generator[Task, None, None]:
        """
        Генератор для ленивой фильтрации по приоритету
        :param priority: Искомый приоритет задачи
        :return: Генератор задач с указанным приоритетом
        """
        for task in self._tasks:
            if task.priority == priority:
                yield task

    def get_ready_tasks(self) -> Generator[Task, None, None]:
        """
        Генератор, возвращающий задачи, готовые к выполнению
        :return: Генератор готовых задач
        """
        for task in self._tasks:
            if task.ready_for_execution:
                yield task
