class TaskError(Exception):
    """Базовый класс для ошибок, связанных с задачами"""

    pass


class InvalidPriorityError(TaskError):
    """Ошибка, возникающая при указании недопустимого приоритета задачи"""

    pass


class InvalidStateError(TaskError):
    """Ошибка, возникающая при некорректном переходе состояний задачи (нарушение инварианта)"""
    
    pass
