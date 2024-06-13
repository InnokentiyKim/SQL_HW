import psycopg2
import configparser
from pprint import pprint


class Clients:

    def __init__(self, connection) -> None:
        self.connection = connection


    @staticmethod
    def create_connection(database='postgres', user='postgres', password='postgres'):
        try:
            conn = psycopg2.connect(database=database, user=user, password=password)
            return conn
        except:
            print("Connection error")


    def create_database(self) -> None:
        with self.connection.cursor() as curr:
            curr.execute("""
                DROP TABLE IF EXISTS client CASCADE;
                DROP TABLE IF EXISTS phones CASCADE;
                """)
            
            curr.execute("""
                CREATE TABLE IF NOT EXISTS client
                (
                    client_id serial PRIMARY KEY,
                    first_name VARCHAR(30) NOT NULL, 
                    last_name VARCHAR(30) NOT NULL,
                    email VARCHAR(40) NOT NULL
                ); 
                """)
            
            curr.execute("""                           
                CREATE TABLE IF NOT EXISTS phones
                (
                    phone_id serial PRIMARY KEY,
                    phone_number VARCHAR(20) DEFAULT NULL,
                    client_id integer REFERENCES client(client_id) ON DELETE CASCADE            
                ); 
                """)
            self.connection.commit()
            print('Database succesfully created!')
        

    def add_client(self, first_name: str, last_name: str, email: str, phones: list[str]=None):
        with self.connection.cursor() as curr:
            curr.execute("""
                INSERT INTO client(first_name, last_name, email)
                VALUES (%s, %s, %s) RETURNING client_id; 
                """, (first_name, last_name, email)
                )
            cur_client_id = curr.fetchone()[0]
            if phones:
                for number in phones:
                    number = number.replace(' ', '')
                    curr.execute("""
                        INSERT INTO phones(phone_number, client_id)
                        VALUES (%s, %s)
                        """, (number, cur_client_id)
                    )
            self.connection.commit()
            print(f'Client with id = {cur_client_id} added')


    def add_phone(self, phone: str, client_id: int):
        with self.connection.cursor() as curr:
            phone = phone.replace(' ', '')
            curr.execute("""
                INSERT INTO phones(phone_number, client_id)
                VALUES (%s, %s);       
                """, (phone, client_id)
            )
            self.connection.commit()

    def change_clients_info(self, client_id: int, first_name: str=None, last_name: str=None, email: str=None, phones: list[str]=None):
        with self.connection.cursor() as curr:
            if first_name:
                curr.execute("""
                    UPDATE client
                    SET first_name = %s
                    WHERE client_id = %s;
                    """, (first_name, client_id)
                )
            if last_name:
                curr.execute("""
                    UPDATE client
                    SET last_name = %s
                    WHERE client_id = %s;
                    """, (last_name, client_id)
                )
            if email:
                curr.execute("""
                    UPDATE client
                    SET email = %s
                    WHERE client_id = %s;
                    """, (email, client_id)
                )
            if phones:
                curr.execute("""
                        DELETE FROM phones
                        WHERE client_id = %s;                       
                        """, (client_id, )
                    )
                for number in phones:
                    number = number.replace(' ', '')
                    curr.execute("""
                        INSERT INTO phones(phone_number, client_id)
                        VALUES (%s, %s);                      
                        """, (number, client_id)
                    ) 
            self.connection.commit()
            print(f"Client's (with id = {client_id}) information updated")

    def delete_phone(self, client_id: int, phone_id: int):
        with self.connection.cursor() as curr:
            curr.execute("""
                DELETE FROM phones
                WHERE client_id = %s AND phone_id = %s
                """, (client_id, phone_id)
            )
            self.connection.commit()
            print(f"Client's (with id = {client_id}) phone number deleted")


    def delete_all_phones(self, client_id: int):
        with self.connection.cursor() as curr:
            curr.execute("""
                DELETE FROM phones
                WHERE client_id = %s
                """, (client_id, )
            )
            self.connection.commit()
            print(f"All phone numbers deleted for client with id = {client_id}")


    def delete_client(self, client_id: int):
        with self.connection.cursor() as curr:
            curr.execute("""
                DELETE FROM client
                WHERE client_id = %s
                """, (client_id, )
            )
            self.connection.commit()
            print(f"Client with id = {client_id} deleted")

    def find_client(self, first_name: str=None, last_name=None, email=None, phone: str=None):
        with self.connection.cursor() as curr:
            if not first_name:
                first_name = '%'
            if not last_name:
                last_name = '%'
            if not email:
                email = '%'
            if not phone:
                phone = '%'
            curr.execute("""
                SELECT client_id, first_name, last_name, email, phone_number
                FROM client
                LEFT JOIN phones using(client_id)
                WHERE first_name LIKE %s AND last_name LIKE %s AND email LIKE %s AND phone_number LIKE %s;
                """, (first_name, last_name, email, phone)
            )
            print("Found client(s):")
            pprint(curr.fetchall())

    def show_all_clients(self, limit=10):
        with self.connection.cursor() as curr:
            curr.execute("""
                SELECT *
                FROM client
                LEFT JOIN phones using(client_id);
                """
            )
            pprint(curr.fetchmany(limit))   


    def show_clients_info(self, client_id: int):
        with self.connection.cursor() as curr:
            curr.execute("""
                SELECT *
                FROM client
                LEFT JOIN phones using(client_id)
                WHERE client_id = %s;
                """, (client_id, )
            )
            pprint(curr.fetchone())  


def main():
    config = configparser.ConfigParser()
    config.read("con_settings.ini")
    conn = Clients.create_connection(database=config['CNS']['database'], user=config['CNS']['user'], password=config['CNS']['password'])
    client = Clients(conn)
    client.create_database()
    client.add_client('Dmitriy', 'Vasilev', 'dmvasil@mail.ru', ['+7 987 902 33 55', '+7 932 822 11 32'])
    client.add_client('Dmitriy', 'Levin', 'Dlevin@ya.ru', ['+7 934 456 52 13'])
    client.add_client('Sergey', 'Demin', 'SDemin@ya.ru', ['+7 913 355 17 19'])
    client.add_client('Ivan', 'Ivanov', 'IvanovI@gmail.com')
    client.add_phone('+7 932 211 12 63', 2)
    client.add_phone('+7 978 434 07 05', 3)
    client.delete_phone(2, 3)
    client.find_client(first_name='Dmitriy', email='dmvasil@mail.ru')
    client.change_clients_info(1, first_name='Grigoriy', email='DGrigory@indox.ru')
    client.add_client('Ivan', 'Ivanov', 'IvanovI_88@gmail.com', ['+7987 902 3355'])
    client.change_clients_info(4, phones=['+7 956 124 78 58', '+7 926 259 62 48'])
    client.show_clients_info(4)
    client.delete_client(3)
    client.delete_phone(4, 7)
    client.delete_all_phones(4)
    client.show_all_clients()
    client.find_client(phone='+79322111263')
    conn.close()

if __name__ == '__main__':
    main()


    