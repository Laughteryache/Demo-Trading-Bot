import sqlite3

conn = sqlite3.connect('test.py')

class Database:
    def __init__(self, name):
        self.name = name

    def create_table(self):
        cur = conn.cursor()
        cur.execute(f"""CREATE TABLE IF NOT EXISTS {self.name}
        (id INT,
        deposit INT,
        positions TEXT)
        ;""")
        conn.commit()
        cur.close()
        print('[INFO] TABLE CREATED SUCCESSFULLY')

    def insert_new_user(self, id):
        cur = conn.cursor()
        cur.execute(f"""INSERT INTO {self.name} (id, deposit, positions) 
        VALUES ({id}, {100000}, '');
        """)
        conn.commit()
        cur.close()
        print('[INFO] USER INSERT SUCCESSFULLY')

    def get_user_info(self, id):
        cur = conn.cursor()
        cur.execute(f"""SELECT deposit, positions FROM {self.name} 
        WHERE id = {id};
        """)
        conn.commit()
        cur.close()
        print('[INFO] USER INFO DROPPED')
