import sqlite3
from config.config import Config, load_config

config: Config = load_config()
conn = sqlite3.connect(config.database.name)


class Database:
    def __init__(self, name):
        self.name = name

    def create_table(self):
        cur = conn.cursor()
        cur.execute(f"""CREATE TABLE IF NOT EXISTS {self.name}
        (user_id INT PRIMARY KEY,
        deposit INT,
        positions TEXT,
        prices TEXT,
        total INT)
        ;""")
        conn.commit()
        cur.close()

    def insert_new_user(self, user_id: int):
        cur = conn.cursor()
        cur.execute(f"""INSERT INTO {self.name} (user_id, deposit, positions, prices, total)
        VALUES ({user_id}, {150000}, 'BTC-0 ETH-0 SOL-0 BNB-0 TON-0 XRP-0 DOGE-0 TRX-0 LINK-0 LTC-0 ATOM-0 ETC-0',
        'BTC-0 ETH-0 SOL-0 BNB-0 TON-0 XRP-0 DOGE-0 TRX-0 LINK-0 LTC-0 ATOM-0 ETC-0', {0});
        """)
        conn.commit()
        cur.close()

    def get_user_statistics(self, user_id: int) -> list:
        cur = conn.cursor()
        cur.execute(f"""SELECT deposit, positions FROM {self.name} 
                WHERE user_id = {user_id};
                """)
        statistics = cur.fetchall()[0]
        if statistics[1]:
            list_of_positions = []
            for i in statistics[1].split():
                pair = i.split('-')
                list_of_positions.append(f'{pair[0]}-{pair[1]}')
            statistics = [statistics[0], list_of_positions]
        else:
            statistics = [statistics[0], ['Открытых позиций нет']]
        conn.commit()
        cur.close()
        return statistics

    def update_user_deposit(self, user_id: int, price: float, quantity: int):
        cur = conn.cursor()
        cur.execute(f"""SELECT deposit FROM {self.name}
                WHERE user_id = {user_id};
                """)
        deposit = cur.fetchone()[0]
        changed = float(deposit)+price*abs(quantity)
        cur.execute(f"""UPDATE {self.name} SET deposit={changed} WHERE user_id={user_id};""")
        conn.commit()
        cur.close()

    def get_user_positions(self, user_id) -> dict:
        cur = conn.cursor()
        cur.execute(f"""SELECT positions FROM {self.name} 
                WHERE user_id = {user_id};
                """)
        data: dict = {}
        positions = cur.fetchall()[0]
        for i in positions[0].split():
            key, value = i.split('-')
            data[key] = value
        conn.commit()
        cur.close()
        return data

    def update_user_positions(self, user_id, position: str, quantity: int):
        cur = conn.cursor()
        cur.execute(f"""SELECT positions FROM {self.name} 
                        WHERE user_id={user_id};
                        """)
        positions = cur.fetchall()[0]
        main_list: list = []
        for i in positions[0].split():
            key, value = i.split('-')
            value = int(value)
            if key == position:
                value += quantity
            main_list.append(f"{key}-{value}")
        positions = ' '.join(main_list)
        cur.execute(f"""UPDATE {self.name} SET positions='{positions}' WHERE user_id={user_id};""")
        conn.commit()
        cur.close()

    def update_prices(self, user_id: int, price: float, name_of_coin: str):
        cur = conn.cursor()
        cur.execute(f"""SELECT prices FROM {self.name}
                        WHERE user_id={user_id};
                        """)
        prices = cur.fetchall()[0]
        main_list: list = []
        for i in prices[0].split():
            key, value = i.split('-')
            value = float(value)
            if key == name_of_coin:
                value = price
            main_list.append(f"{key}-{value}")
        positions = ' '.join(main_list)
        cur.execute(f"""UPDATE {self.name} SET prices='{positions}' WHERE user_id={user_id};""")
        conn.commit()
        cur.close()

    def update_total(self, user_id: int):
        cur = conn.cursor()
        cur.execute(f"""SELECT total FROM {self.name}
                        WHERE user_id={user_id};
                        """)
        total = cur.fetchall()[0][0]
        total += 1
        cur.execute(f"""UPDATE {self.name} SET total={total} WHERE user_id={user_id};""")
        conn.commit()
        cur.close()

    def get_total(self, user_id: int) -> int:
        cur = conn.cursor()
        cur.execute(f"""SELECT total FROM {self.name}
                        WHERE user_id={user_id};
                        """)
        result = cur.fetchall()[0][0]
        conn.commit()
        cur.close()
        return result

    def clear_all(self, user_id: int):
        cur = conn.cursor()
        cur.execute(f"""UPDATE {self.name} SET deposit={150000},
                        positions='BTC-0 ETH-0 SOL-0 BNB-0 TON-0 XRP-0 DOGE-0 TRX-0 LINK-0 LTC-0 ATOM-0 ETC-0',
                        total={0},
                        prices='BTC-0 ETH-0 SOL-0 BNB-0 TON-0 XRP-0 DOGE-0 TRX-0 LINK-0 LTC-0 ATOM-0 ETC-0'
                        WHERE user_id={user_id};
                        """)
        conn.commit()
        cur.close()
