import logging


def registros(
    fname="seviper.log",
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
):
    logger = logging.getLogger()

    if not logger.hasHandlers():
        # Por padrão já está definido a configuração básica do log
        logging.basicConfig(filename=fname, level=level, format=format, datefmt=datefmt)

        # Definindo o formato do log e nível a ser retornado no .log e terminal
        console = logging.StreamHandler()
        console.setLevel(level=level)
        console.setFormatter(logging.Formatter(fmt=format, datefmt=datefmt))

        logging.getLogger().addHandler(console)

    return logging
