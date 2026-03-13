import logging


def setup_logging():
    """
    Создание конфига логирования
    """
    logging.basicConfig(
        filename="shell.log",
        level=logging.INFO,
        format="[%(asctime)s] %(message)s",
        datefmt="%y-%m-%d %H:%M:%S",
        encoding="utf-8",
    )
