import sqlite3
conn = sqlite3.connect('test2.py')


class Database:
    def __init__(self, name):
        self.name = name

    def create_table(self):
        cur = conn.cursor()
        cur.execute(f"""CREATE TABLE IF NOT EXISTS {self.name}
        (id INT PRIMARY KEY,
        deposit INT,
        positions TEXT, 
        page INT)
        ;""")
        conn.commit()
        cur.close()
        print('[INFO] TABLE CREATED SUCCESSFULLY')

    def insert_new_user(self, id):
        cur = conn.cursor()
        cur.execute(f"""INSERT INTO {self.name} (id, deposit, positions, page) 
        VALUES ({id}, {100000}, '', 0);
        """)
        conn.commit()
        cur.close()
        print('[INFO] USER INSERT SUCCESSFULLY')

    def get_user_statistics(self, id):
        cur = conn.cursor()
        cur.execute(f"""SELECT deposit, positions FROM {self.name} 
                WHERE id = {id};
                """)
        statistics = cur.fetchall()[0]
        if statistics[1]:
            list_of_positions = []
            for i in statistics[1].split():
                pair = i.split('-')
                list_of_positions.append(f'{pair[0]} - {pair[1]}')
            statistics = [statistics[0], list_of_positions]
        else:
            statistics = [statistics[0], ['Открытых позиций нет']]
        conn.commit()
        cur.close()
        print('[INFO] USER INFO DROPPED')
        return statistics

    def get_user_page(self, id):
        cur = conn.cursor()
        cur.execute(f"""SELECT page FROM {self.name} 
                        WHERE id = {id};
                        """)
        page = cur.fetchall()[0][0]
        conn.commit()
        cur.close()
        print('[INFO] USER PAGE DROPPED')
        return page

    def update_user_page(self, id, page):
        cur = conn.cursor()
        cur.execute(f"""UPDATE {self.name}
                    SET page={page} WHERE id={id}""")
        conn.commit()
        cur.close()
        print('[INFO] USER PAGE UPDATED')

    def update_user_deposit(self, id):
        pass

    def update_user_briefcase(self, id):
        pass