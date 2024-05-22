import logging
import sys


def get_logger(name: str):
    logging.basicConfig(stream=sys.stdout,
                        level=logging.DEBUG,
                        datefmt='%Y-%m-%d %H:%M:%S',
                        format='%(asctime)s %(name)s - %(levelname)s - %(message)s')

    return logging.getLogger(name)
