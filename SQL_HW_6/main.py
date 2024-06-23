import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from models import *
import configparser
import json


def separate_values(sep=' | '):
    def decor(func):
        def wrapper(*args, **kwargs):
            query_res = func(*args, **kwargs)
            if query_res:
                column_width = [0] * len(query_res[0])
                for line in query_res:
                    for ind, item in enumerate(line):
                        if len(str(item)) > column_width[ind]:
                            column_width[ind] = len(str(item))
                for record in query_res:
                    res_line = []
                    for ind, item in enumerate(record):
                        res_line.append(str(item).ljust(column_width[ind]))
                    print(sep.join(res_line))
        return wrapper
    return decor


@separate_values()
def get_info_by_publisher(session, publisher_id: int=None):
    if publisher_id:
        query_res = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale) \
            .join(Publisher, Publisher.id == Book.id_publisher) \
            .join(Stock, Stock.id_book == Book.id).join(Shop, Shop.id == Stock.id_shop) \
            .join(Sale, Sale.id_stock == Stock.id) \
            .filter(Publisher.id == publisher_id).all()
    else:
        publisher_name = input("Введите издателя: ")
        query_res = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale) \
            .join(Publisher, Publisher.id == Book.id_publisher) \
            .join(Stock, Stock.id_book == Book.id).join(Shop, Shop.id == Stock.id_shop) \
            .join(Sale, Sale.id_stock == Stock.id) \
            .filter(Publisher.name == publisher_name).all()
    return tuple(query_res)


config = configparser.ConfigParser()
config.read("SQL_HW_6/settings.ini")
dialect = config['CNS']['dialect']
user_name = config['CNS']['user_name']
password = config['CNS']['password']
url = config['CNS']['url']
port = config['CNS']['port']
db_name = config['CNS']['db_name']
DSN = f'{dialect}://{user_name}:{password}@{url}:{port}/{db_name}'
engine = sq.create_engine(DSN)
create_tables(engine)
Session = sessionmaker(bind=engine)
session = Session()
with open('SQL_HW_6/tests_data.json') as td:
    test_data = json.load(td)
models = {'publisher': Publisher, 'shop': Shop, 'book': Book, 'stock': Stock, 'sale': Sale}    
for line in test_data:
    model = models[line.get('model')]
    session.add(model(id=line.get('pk'), **line.get('fields')))
session.commit()
get_info_by_publisher(session)
session.close()