import sqlite3
from datetime import timedelta

class DB_HANDLER:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def db_connect(self):
        if not self.conn:
            self.conn = sqlite3.connect("database.db")
            self.cursor = self.conn.cursor()

    def db_disconnect(self):
        self.conn.close()

    def db_create(self):
        self.db_connect()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS entrances (
                    id INTEGER PRIMARY KEY,
                    card_id INTEGER NOT NULL,
                    pools_zone INTEGER,
                    sauna_zone INTEGER,
                    playground_zone INTEGER,
                    valid_time INTEGER NOT NULL,
                    purchase_time DATETIME NOT NULL
            )
        ''')

        self.conn.commit()
        self.db_disconnect()

    def db_insert_entrance(self, card_id, pools_zone, sauna_zone, playground_zone, valid_time, purchase_time):
        self.cursor.execute('''INSERT INTO entrances(card_id, pools_zone, sauna_zone, playground_zone, valid_time, purchase_time)
                    VALUES (?, ?, ?, ?, ?, ?)''',
                    (card_id, pools_zone, sauna_zone, playground_zone, valid_time, purchase_time))
        self.conn.commit()
        return f"Ticket saved to database. It is valid until {purchase_time + timedelta(minutes=valid_time)}."

    def latest_ticket(self, rfid):
        self.db_connect()
        self.cursor.execute("SELECT * FROM entrances WHERE card_id = ? ORDER BY purchase_time DESC LIMIT 1", (rfid,))
        result = self.cursor.fetchone()
        self.db_disconnect()
        return result
 

if __name__ == "__main__":
    db = DB_HANDLER()
    db.db_create()




