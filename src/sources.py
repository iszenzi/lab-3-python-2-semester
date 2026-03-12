import json
import random
from src.task import Task


class FileTaskSource:
    def __init__(self, path: str):
        if not isinstance(path, str):
            raise TypeError("Путь к файлу должен быть строкой")
        self.path = path

    def get_tasks(self) -> list[Task]:
        try:
            tasks = []
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for i in data:
                tasks.append(Task(id=i["id"], payload=i["payload"]))
            return tasks
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл {self.path} не найден")


class GeneratorTaskSource:
    def __init__(self, count: int = 10, seed: int | None = None):
        if not isinstance(count, int) or count <= 0:
            raise TypeError("Количество задач должно быть целым положительным числом")
        if seed is not None and not isinstance(seed, int):
            raise TypeError("Seed должен быть целым числом или None")
        self.count = count
        self._random = random.Random(seed)

    def get_tasks(self) -> list[Task]:
        tasks = []
        tasks_type = [
            "process_order",
            "send_notification",
            "recalculate_stats",
            "check_resource",
            "ingest_external",
            "send_email",
            "send_sms",
            "push_notification",
            "call_api",
            "generate_report",
            "data_processing",
            "update_database",
            "monitoring_task",
            "logging_task",
            "validation_task",
            "integration_task",
        ]
        for i in range(self.count):
            task_type = tasks_type[i % len(tasks_type)]
            tasks.append(
                Task(
                    id=i + 1,
                    payload={
                        "type": task_type,
                        "sequence": i + 1,
                        "priority": self._random.randint(1, 5),
                    },
                )
            )
        return tasks


class ApiTaskSource:
    def __init__(self):
        self._api_data = [
            {"id": 1, "payload": {"type": "process_order", "priority": 3}},
            {"id": 2, "payload": {"type": "send_notification", "priority": 2}},
            {"id": 3, "payload": {"type": "recalculate_stats", "priority": 4}},
        ]

    def get_tasks(self) -> list[Task]:
        tasks = []
        for i in self._api_data:
            tasks.append(Task(id=i["id"], payload=i["payload"]))
        return tasks
