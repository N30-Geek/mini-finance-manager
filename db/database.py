import os, pathlib
from config import DB_PATH 
import sqlite3 
from datetime import datetime

class Database:
    def __init__(self):

        # Checking the existance database file and create it if not existe
        if not os.path.isfile(DB_PATH):     
            self.conn = sqlite3.connect(DB_PATH)
        # Main variables 
        self.cur = self.conn.cursor()
        self.current_date = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
        
        # init methods
        self.init_db() # initialise the data base

    def init_db(self):
        """This method initilize the data base Return:  bool : True or False"""
        try:
            # Creatting users tables
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS users_accounts(
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_name TEXT NOT NULL,
                    user_email TEXT NOT NULL,
                    user_login TEXT NOT NULL,
                    user_password TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    is_deleted TEXT NOT NULL,
                )
            """)

            #Creatting  accounts table
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS accounts (
                    account_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    account_name TEXT NOT NULL,
                    account_init_solde REAL NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)
            # creatting categories table
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS categories (
                    cat_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cat_name TEXT NOT NULL,
                    cat_type TEXT NOT NULL,
                    cat_icon TEXT NOT NULL
                )
            """)
            
            # creatting transactions table
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
    
    def add_user(self, user_name : str, user_email : str,  user_login: str, user_password: str) -> bool:
        """this method adding a new user in the dataabse
        ** Parameters: 
            user_name  : str 
            user_login : str 
            user_email : str 
            user_password : str
            created_at  : str 
        ** Returns: 
            bool : True if user was saved successfully
        """
        _user_datas = (user_name, user_email, user_login, user_password, self.current_date)

        try:
            # Trying to add user data in db
            self.cur.execute("""
                INSERT INTO users(
                    user_name, 
                    user_email,
                    user_login, 
                    user_password, 
                    created_at) 
                VALUES (?, ?, ?, ?, ?)
            """, _user_datas)

            self.conn.commit()
            self._close()
            return True

        except Exception as e:
            print("Error: " , e)
            return False

    def _close(self):
        self.conn.close()
