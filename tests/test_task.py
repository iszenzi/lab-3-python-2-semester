import pytest
from src.exceptions import InvalidPriorityError, InvalidStateError, TaskError
from src.task import Task, TaskStatus


class TestTask:
    def test_task_creation(self):
        """
        Проверяет создание задачи
        """
        task = Task(id=1, payload={}, description="Test task")
        assert task.id == 1
        assert task.status == TaskStatus.NEW
        assert task.priority == 3
        assert task.description == "Test task"
        assert task.ready_for_execution

    def test_task_priority_validation(self):
        """
        Проверяет валидацию приоритета через дескриптор
        """
        task = Task(id=1, payload={}, description="Priority task")
        task.priority = 5
        assert task.priority == 5

        with pytest.raises(InvalidPriorityError) as exc_info:
            task.priority = 6
        assert "Приоритет должен быть в диапазоне от 1 до 5" in str(exc_info.value)
        assert exc_info.type is InvalidPriorityError

        with pytest.raises(InvalidPriorityError) as exc_info:
            task.priority = 0
        assert "Приоритет должен быть в диапазоне от 1 до 5" in str(exc_info.value)
        assert exc_info.type is InvalidPriorityError

        with pytest.raises(InvalidPriorityError) as exc_info:
            task.priority = "3"
        assert "Приоритет должен быть целым числом, получено: str" in str(
            exc_info.value
        )
        assert exc_info.type is InvalidPriorityError

    def test_task_default_description(self):
        """
        Проверяет, что у задачи без описания устанавливается значение по умолчанию
        """
        task = Task(id=1, payload={})
        assert task.description == "Без описания"

    def test_task_state_transitions(self):
        """
        Проверяет успешные переходы состояний задачи (NEW -> IN_PROGRESS -> COMPLETED)
        """
        task = Task(id=1, payload={})

        task.start()
        assert task.status == TaskStatus.IN_PROGRESS

        task.complete()
        assert task.status == TaskStatus.COMPLETED

    def test_task_fail_transition(self):
        """
        Проверяет успешный переход состояния задачи в FAILED
        """
        task = Task(id=1, payload={})
        task.start()
        task.fail()
        assert task.status == TaskStatus.FAILED

    def test_invalid_state_transitions(self):
        """
        Проверяет, что недопустимые переходы состояний вызывают InvalidStateError
        """
        task = Task(id=1, payload={})

        with pytest.raises(InvalidStateError) as exc_info:
            task.complete()
        assert "Завершить можно только начатую задачу" in str(exc_info.value)
        assert exc_info.type is InvalidStateError

        task.start()
        task.complete()

        with pytest.raises(InvalidStateError) as exc_info:
            task.start()
        assert "Нельзя запустить задачу в статусе" in str(exc_info.value)
        assert exc_info.type is InvalidStateError

        with pytest.raises(InvalidStateError) as exc_info:
            task.fail()
        assert "Завершить с ошибкой можно только начатую или новую задачу" in str(
            exc_info.value
        )
        assert exc_info.type is InvalidStateError

    def test_read_only_properties(self):
        """
        Проверяет, что поля id, status и created_at защищены от записи
        """
        task = Task(id=1, payload={})

        with pytest.raises(AttributeError) as exc_info:
            task.id = 2
        assert exc_info.type is AttributeError

        with pytest.raises(AttributeError) as exc_info:
            task.status = TaskStatus.IN_PROGRESS
        assert exc_info.type is AttributeError

        with pytest.raises(AttributeError) as exc_info:
            task.created_at = "now"
        assert exc_info.type is AttributeError

    def test_ready_for_execution(self):
        """
        Проверяет работу вычисляемого свойства ready_for_execution
        """
        task = Task(id=1, payload={})
        assert task.ready_for_execution

        task.start()
        assert not task.ready_for_execution
