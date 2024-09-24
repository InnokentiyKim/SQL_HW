from functools import wraps


def cached(func):
    """
    Декоратор для хранения результатов функции в кэше.
    """
    cache = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key in cache:
            return cache[key]
        result = func(*args, **kwargs)
        cache[key] = result
        return result
    return wrapper
