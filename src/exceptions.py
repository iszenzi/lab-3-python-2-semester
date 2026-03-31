class TaskError(Exception):
    """Базовый класс для ошибок, связанных с задачами"""

    pass


class InvalidPriorityError(TaskError):
    """Ошибка, возникающая при указании недопустимого приоритета задачи"""

    pass
