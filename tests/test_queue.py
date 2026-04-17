import pytest
from typing import Generator

from src.task import Task, TaskStatus
from src.queue import TaskQueue, TaskQueueIterator


@pytest.fixture
def sample_tasks() -> list[Task]:
    """
    Фикстура, создающая список базовых задач для тестов
    """
    t1 = Task(id=1, payload={"data": 1}, priority=1)

    t2 = Task(id=2, payload={"data": 2}, priority=3)
    t2.start()  # Статус IN_PROGRESS

    t3 = Task(id=3, payload={"data": 3}, priority=5)

    t4 = Task(id=4, payload={"data": 4}, priority=1)
    t4.start()
    t4.complete()  # Статус COMPLETED

    return [t1, t2, t3, t4]


def test_task_queue_initialization() -> None:
    """
    Проверка инициализации пустой очереди
    """
    queue = TaskQueue()
    assert len(queue) == 0


def test_task_queue_add_extend(sample_tasks: list[Task]) -> None:
    """
    Проверка добавления и расширения списка задач
    """
    queue = TaskQueue()
    queue.add_task(sample_tasks[0])
    assert len(queue) == 1

    queue.extend_tasks(sample_tasks[1:])
    assert len(queue) == 4


def test_task_queue_iterator(sample_tasks: list[Task]) -> None:
    """
    Проверка пользовательского итератора и выброса StopIteration
    """
    queue = TaskQueue(sample_tasks)
    iterator = iter(queue)

    assert isinstance(iterator, TaskQueueIterator)

    assert iter(iterator) is iterator

    assert next(iterator) == sample_tasks[0]
    assert next(iterator) == sample_tasks[1]
    assert next(iterator) == sample_tasks[2]
    assert next(iterator) == sample_tasks[3]

    with pytest.raises(StopIteration):
        next(iterator)


def test_task_queue_multiple_iterations(sample_tasks: list[Task]) -> None:
    """
    Проверка многократного обхода коллекции (создание новых итераторов)
    """
    queue = TaskQueue(sample_tasks)

    first_pass = list(queue)
    second_pass = list(queue)

    assert first_pass == sample_tasks
    assert second_pass == sample_tasks


def test_filter_by_status_generator(sample_tasks: list[Task]) -> None:
    """
    Проверка ленивой фильтрации по статусу задачи
    """
    queue = TaskQueue(sample_tasks)
    gen = queue.filter_by_status(TaskStatus.IN_PROGRESS)

    assert isinstance(gen, Generator)

    filtered = list(gen)
    assert len(filtered) == 1
    assert filtered[0].id == 2


def test_filter_by_priority_generator(sample_tasks: list[Task]) -> None:
    """
    Проверка ленивой фильтрации по приоритету
    """
    queue = TaskQueue(sample_tasks)
    gen = queue.filter_by_priority(1)

    assert isinstance(gen, Generator)

    filtered = list(gen)
    assert len(filtered) == 2
    assert [t.id for t in filtered] == [1, 4]


def test_get_ready_tasks_generator(sample_tasks: list[Task]) -> None:
    """
    Проверка фильтрации задач, готовых к выполнению (NEW)
    """
    queue = TaskQueue(sample_tasks)
    gen = queue.get_ready_tasks()

    assert isinstance(gen, Generator)

    filtered = list(gen)
    assert len(filtered) == 2
    assert [t.id for t in filtered] == [1, 3]


def test_lazy_evaluation() -> None:
    """
    Проверка того, что фильтрация происходит лениво
    (данные не выкачиваются все сразу)
    """
    tasks = [
        Task(id=i, payload={}, priority=1 if i % 2 == 0 else 5) for i in range(1, 100)
    ]
    queue = TaskQueue(tasks)

    gen = queue.filter_by_priority(1)
    first_match = next(gen)

    assert first_match.id == 2
