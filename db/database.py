import os, pathlib
from config import DB_PATH 
import sqlite3 
from datetime import datetime

class Database:
    def __init__(self):

        # Checking the existance database file and create it if not existe
        if os.path.isfile(DB_PATH):     
            self.conn = sqlite3.connect(DB_PATH)
        else:
            self.conn = sqlite3.connect(pathlib.Path(__file__).parent/"db/db.db")
        # cursor
        self.cur = self.conn.cursor()

        # Main variables 
        self.current_date = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
        
        # init methods
        self.init_db() # initialise the data base

    def init_db(self):

        try:
            # Creation de l
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS users(
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_name TEXT NOT NULL,
                    user_login_login TEXT NOT NULL,
                    user_password TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS accounts (
                    account_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    account_name TEXT NOT NULL,
                    account_init_solde REAL NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS categories (
                    cat_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cat_name TEXT NOT NULL,
                    cat_type TEXT NOT NULL,
                    cat_icon TEXT NOT NULL
                )
            """)
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    trans_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    trans_date TEXT NOT NULL,
                    trans_description TEXT,
                    trans_amount REAL NOT NULL,
                    trans_type TEXT NOT NULL,
                    category_id INTEGER NOT NULL,
                    account_id INTEGER NOT NULL,
                    FOREIGN KEY (category_id) REFERENCES categories (trans_id),
                    FOREIGN KEY (account_id) REFERENCES accounts (trans_id)
                )
            """)
            self.conn.commit()
            
            return True
        except Exception as e:
            print("Error where initialising the database : ", e)
        

    def _close(self):
        self.conn.close()