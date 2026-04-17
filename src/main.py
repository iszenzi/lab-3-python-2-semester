from dataclasses import asdict
import json
import typer
from pathlib import Path
from src.loader import TaskLoader
from src.sources import ApiTaskSource, FileTaskSource, GeneratorTaskSource
from src.task import Task, TaskStatus
from src.queue import TaskQueue
from src.protocol import TaskSource
import logging
from src.logger import setup_logging

cli = typer.Typer(no_args_is_help=True)


def print_tasks(tasks: list[Task]) -> None:
    """
    Печатает список задач
    :param tasks: Список задач
    """
    for task in tasks:
        task_dict = {
            "id": task.id,
            "payload": task.payload,
            "priority": task.priority,
            "status": task.status.value,
            "description": task.description,
            "created_at": task.created_at.isoformat(),
        }
        print(json.dumps(task_dict, ensure_ascii=False))


SOURCE_REGISTRY: dict[str, type[TaskSource]] = {
    "file": FileTaskSource,
    "generator": GeneratorTaskSource,
    "api": ApiTaskSource,
}


@cli.command("sources")
def sources_list() -> None:
    """
    Печатает доступные источники
    """
    print("Доступные источники:")
    for source in SOURCE_REGISTRY:
        print(f"- {source}")


@cli.command("read")
def read(
    file: list[Path] = typer.Option(
        default_factory=list,
        exists=True,
        dir_okay=False,
        readable=True,
        help="Читать задачи из JSON-файла (можно несколько раз)",
    ),
    generator: int | None = typer.Option(
        None,
        "--generator",
        min=1,
        help="Сгенерировать N задач",
    ),
    seed: int | None = typer.Option(
        None,
        "--seed",
        help="Seed для генератора",
    ),
    api: bool = typer.Option(
        False,
        "--api",
        help="Читать задачи из API-заглушки",
    ),
) -> None:
    """
    Загружает задачи и выводит их в консоль
    :param file: Список файлов с задачами
    :param generator: Количество задач для генератора
    :param seed: Seed для генератора
    :param api: Использовать API-заглушку
    """
    sources: list[TaskSource] = []
    for path in file:
        sources.append(FileTaskSource(str(path)))
    if generator is not None:
        sources.append(GeneratorTaskSource(count=generator, seed=seed))
    if api:
        sources.append(ApiTaskSource())

    loader = TaskLoader(sources)
    grouped = loader.load_tasks()

    total = 0
    for source, tasks in grouped:
        if isinstance(source, FileTaskSource):
            source_title = f"файл {source.path}"
        elif isinstance(source, GeneratorTaskSource):
            source_title = f"генератор count={source.count} seed={source.seed}"
        else:
            source_title = "api-заглушка"

        print(f"Источник: {source_title}")
        print_tasks(tasks)
        print("")
        total += len(tasks)

    print(f"\nВсего: {total}")


@cli.command("process")
def process(
    file: list[Path] = typer.Option(
        default_factory=list,
        exists=True,
        dir_okay=False,
        readable=True,
        help="Читать задачи из JSON-файла (можно несколько раз)",
    ),
    generator: int | None = typer.Option(
        None,
        "--generator",
        min=1,
        help="Сгенерировать N задач",
    ),
    seed: int | None = typer.Option(
        None,
        "--seed",
        help="Seed для генератора",
    ),
    api: bool = typer.Option(
        False,
        "--api",
        help="Читать задачи из API-заглушки",
    ),
    status: TaskStatus | None = typer.Option(
        None,
        "--status",
        help="Поиск задач по статусу (после обработки)",
    ),
    priority: int | None = typer.Option(
        None,
        "--priority",
        help="Поиск задач по приоритету",
    ),
) -> None:
    """
    Загружает задачи в очередь и обрабатывает их, меняя статусы
    """
    sources: list[TaskSource] = []
    for path in file:
        sources.append(FileTaskSource(str(path)))
    if generator is not None:
        sources.append(GeneratorTaskSource(count=generator, seed=seed))
    if api:
        sources.append(ApiTaskSource())

    loader = TaskLoader(sources)
    all_tasks = []

    for _, tasks in loader.load_tasks():
        all_tasks.extend(tasks)

    if not all_tasks:
        logging.warning("Нет задач для загрузки.")
        return

    queue = TaskQueue(all_tasks)
    logging.info(f"Очередь создана. Всего элементов: {len(queue)}\n")

    logging.info("Начинаем обработку задач...")
    for task in queue.get_ready_tasks():
        logging.info(f"Задача #{task.id} (Приоритет: {task.priority})")

        task.start()
        logging.info(f"  -> Взята в работу. Новый статус: {task.status.value}")

        task.complete()
        logging.info(f"  -> Успешно завершена. Новый статус: {task.status.value}\n")

    logging.info("Обработка завершена.\n")

    if status is not None:
        logging.info(f"--- Задачи со статусом {status.value} ---")
        status_gen = queue.filter_by_status(status)
        for t in status_gen:
            logging.info(f"ID: {t.id}, Приоритет: {t.priority}")
        logging.info("---------------------------------------")

    if priority is not None:
        logging.info(f"--- Задачи с приоритетом {priority} ---")
        priority_gen = queue.filter_by_priority(priority)
        for t in priority_gen:
            logging.info(f"ID: {t.id}, Статус: {t.status.value}")
        logging.info("---------------------------------------")


def main() -> None:
    """
    Запускает CLI`
    """
    cli()


if __name__ == "__main__":
    setup_logging()
    main()
