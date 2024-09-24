import logging
from logging.handlers import RotatingFileHandler
from functools import wraps


LOGGER_PATH = 'bot_logging/bot.log'

"""
Логирование ошибок
"""
error_logger = logging.getLogger('error_logger')
error_logger.setLevel(logging.ERROR)
error_handler = RotatingFileHandler(LOGGER_PATH, maxBytes=10000000, backupCount=5)
formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s',
                              datefmt='%d-%m-%Y %H:%M:%S')
error_handler.setFormatter(formatter)
error_logger.addHandler(error_handler)


def error_logging(path, exc_info=False):
    """
    Декоратор для логирования ошибок.
    """
    __logger = logging.getLogger('bot_logger')
    __logger.setLevel(logging.ERROR)
    handler = RotatingFileHandler(path, maxBytes=10000000, backupCount=5)
    formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s',
                                  datefmt='%d-%m-%Y %H:%M:%S')
    handler.setFormatter(formatter)
    __logger.addHandler(handler)
    def _logging(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except Exception as error:
                __logger.error(f'Вызов функции {function.__name__} с параметрами {args}, {kwargs} '
                               f'вызвал ошибку {error}', exc_info=exc_info)
        return wrapper
    return _logging
