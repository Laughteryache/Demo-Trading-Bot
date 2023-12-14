import psycopg2

conn = psycopg2.connect(user='postgre', password='1234')

print()
class database:
    def __init__(self, name):
        self.name = name

    def create_table(self):
        with conn.cursor() as cur:
            cur.execute(f"""CREATE TABLE IF NOT EXISTS {self.name}
            (id INT PRIMARY KEY,
            bank INT)
            ;""")
            print('[INFO] TABLE CREATED SUCCESSFULLY')

    def insert_new_user(self, id):
        with conn.cursor() as cur:
            cur.execute(f"""INSERT INTO {self.name} (id, bank) 
            VALUES ({id}, {100});
            """)
            print('[INFO] USER INSERT SUCCESSFULLY')

    def get_user_info(self, id):
        with conn.cursor() as cur:
            cur.execute(f"""SELECT bank FROM {self.name} 
            WHERE id = {id};
            """)
            print('[INFO] USER INFO DROPPED')
