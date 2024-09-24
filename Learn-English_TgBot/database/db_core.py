from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from settings.config import settings


class Base(DeclarativeBase):
    """
        Базовый класс для всех таблиц в базе данных.
        Реализует метод `__repr__` для вывода информации о классе и его атрибутах.
        """
    def __repr__(self):

        cols = []
        for col in self.__table__.columns.keys():
            cols.append(f"{col} = {getattr(self, col)}")
        return f"<{self.__class__.__name__} {', '.join(cols)}>"


engine = create_engine(settings.DSN)
Session = sessionmaker(bind=engine, autocommit=False, expire_on_commit=False)


class Singleton(type):
    """
    Метакласс, реализующий паттерн Singleton.
    Гарантирует, что класс, использующий этот метакласс, будет иметь только один экземпляр.
    Атрибуты:
        _instance: Хранит единственный экземпляр класса.
    Методы:
        __call__: Переопределенный метод, возвращающий единственный экземпляр класса.
    """
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = None

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
        return cls.__instance
