import psycopg2


class Client:
    def __init__(self, first_name: str, last_name: str, email: str, phones list[str]=None) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phones

    @staticmethod
    def create_connection(database, user='postgres', password='postgres'):
        try:
            with psycopg2.connect(database=database, user=user, password=password) as conn:
                with conn.cursor() as curr:
                    pass
        except:
            print("Connection error")



    def create_database(self, connection):
        with connection.cursor() as curr:
            curr.executemany("""
                CREATE TABLE IF NOT EXISTS client
                (
                    client_id serial PRIMARY KEY,
                    first_name VARCHAR(30) NOT NULL, 
                    second_name VARCHAR(30) NOT NULL,
                    email VARCHAR(40) NOT NULL,  
                );
                             
                CREATE TABLE IF NOT EXISTS phones:
                (
                    phone_id serial PRIMARY KEY,
                    phone_number VARCHAR(20) SET DEFAULT NULL,
                    client_id integer REFERENCES client(client_id)             
                );
                """
            )
            connection.commit()
        

    def add_client(self, connection, first_name, last_name, email, phones):
        with connection.cursor() as curr:
            curr.execute("""
                INSERT INTO client(first_name, last_name, email)
                VALUES (%s, %s, %s, %s) RETURNING client_id; 
                """, (first_name, last_name, email)
            )
            cur_client_id = curr.fetchone()
            if phones:
                for number in phones:
                    curr.execute("""
                        INSERT INTO phones(phone_number, client_id)
                        VALUES (%s, %s)
                        """, (number, cur_client_id)
                    )
                    print(curr.fetchone())
            else:
                curr.execute("""
                    INSERT INTO phones(client_id)
                    VALUES (%s);
                    """, (cur_client_id)
                )
                connection.commit()


    def add_phone(connection, client_id: int, phone: str):
        with connection.cursor() as curr:
            curr.execute("""
                INSERT INTO phones(client_id, phone)
                VALUES (%s, %s);       
                """, (client_id, phone)
            )

    def change_clients_info(connection, client_id, first_name=None, last_name=None, email=None, phones=None):
        with connection.cursor() as curr:
            curr.execute("""
                UPDATE client
                SET first_name = %s, last_name = %s, email = %s
                WHERE client_id = %s;
                """, (first_name, last_name, email, client_id)
            )
            print(curr.fetchone())
            if phones:
                for number in phones:
                    curr.execute("""
                        UPDATE phones
                        SET phone_number = %s
                        WHERE client_id = %s;                       
                        """, (number, client_id)
                    ) 
                    print(curr.fetchone())

    def delete_phone(connection, client_id, phone_id):
        with connection.cursor() as curr:
            curr.execute("""
                DELETE FROM phones
                WHERE client_id = %s AND phone_id = %s
                """, (client_id, phone_id)
            )
            connection.commit()

    def delete_client(connection, client_id):
        with connection.cursor() as curr:
            curr.execute("""
                DELETE FROM clients
                WHERE client_id = %s
                ON DELETE CASCADE
                """, (client_id)
            )
            connection.commit()

    def find_client(connection, first_name=None, last_name=None, email=None, phone_number=None):
        with connection.cursor() as curr:
            curr.execute("""
                SELECT (first_name, last_name, email, phone)
                FROM client
                JOIN phones using(client_id)
                WHERE first_name = %d OR last_name = %s OR email = %s OR phone_number = %s
                """, (first_name, last_name, email, phone_number)
            )
            print(curr.fetchone())

conn = psycopg2.connect()

    