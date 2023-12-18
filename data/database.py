import sqlite3
conn = sqlite3.connect('test.py')


class Database:
    def __init__(self, name):
        self.name = name

    def create_table(self):
        cur = conn.cursor()
        cur.execute(f"""CREATE TABLE IF NOT EXISTS {self.name}
        (id INT PRIMARY KEY,
        deposit INT,
        positions TEXT,
        total INT,
        wins INT,
        loses INT)
        ;""")
        conn.commit()
        cur.close()
        print('[INFO] TABLE CREATED SUCCESSFULLY')

    def insert_new_user(self, id: int):
        cur = conn.cursor()
        cur.execute(f"""INSERT INTO {self.name} (id, deposit, positions, total, wins, loses)
        VALUES ({id}, {100000}, '', {0}, {0}, {0});
        """)
        conn.commit()
        cur.close()
        print('[INFO] USER INSERT SUCCESSFULLY')

    def get_user_statistics(self, id: int) -> list:
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

    # def get_user_winrate(self, id):
    #     cur = conn.cursor()
    #     cur.execute(f"""SELECT total, wins, loses FROM {self.name}
    #                         WHERE id = {id};
    #                         """)
    #     total, wins, loses = cur.fetchall()[0]
    #     winrate = int(total/wins)
    #     conn.commit()
    #     cur.close()
    #     print('[INFO] USER STATISTICS DROPPED')
    #     return

    def update_user_deposit(self, id: int, price_of_purchase: int):
        cur = conn.cursor()
        cur.execute(f"""SELECT deposit FROM {self.name}
                WHERE id = {id};
                """)
        deposit = cur.fetchall()[0]
        changed = deposit+price_of_purchase
        cur.execute(f"""UPDATE {self.name} SET deposit={changed} WHERE id = {id}""")
        conn.commit()
        cur.close()
        print('[INFO] USER DEPOSIT UPDATE')

    def get_user_deposit(self, id):
        cur = conn.cursor()
        cur.execute(f"""SELECT deposit FROM {self.name}
                WHERE id = {id};
                """)
        deposit = cur.fetchall()[0]
        conn.commit()
        cur.close()
        return deposit

    def get_user_positions(self, id) -> dict:
        cur = conn.cursor()
        cur.execute(f"""SELECT positions FROM {self.name} 
                WHERE id = {id};
                """)
        data: dict = {}
        positions = cur.fetchall()[0].split()
        for i in positions:
            key, value = i.split('-')
            data[key] = value
        conn.commit()
        cur.close()
        return data

    def update_user_briefcase(self, id):
        pass