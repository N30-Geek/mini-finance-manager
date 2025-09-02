from config import DB_PATH 
import sqlite3 
from datetime import datetime

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()

        self.current_date = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
        self.create_tables()
    
    def create_tables(self):
        with open("db_structure") as f:
            sql = f.read()
            self.cursor.executescript(sql)
            self.conn.commit()
    
    def _close(self):
        self.conn.close()
    
    def add_account(self, account_name, account_init_solde):
        sql = "INSERT INTO accounts (account_name, account_init_solde, created_at) VALUES (?, ?, ?)"
        try:
            self.cursor.execute(sql, (account_name, account_init_solde, self.current_date))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            return None