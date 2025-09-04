import unittest
import os
import sqlite3
from datetime import datetime
from unittest.mock import patch, MagicMock

# Add parent directory to path to allow importing db.database
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from db.database import Database

class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test database before any tests run."""
        cls.test_db = "/tmp/test_database.db"
        os.environ["DB_PATH"] = cls.test_db
        # Create a fresh db_structure file with UNIQUE constraint
        with open("/tmp/db_structure", "w") as f:
            f.write("""
            CREATE TABLE IF NOT EXISTS accounts (
                account_id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_name TEXT NOT NULL UNIQUE,
                account_init_solde REAL NOT NULL,
                created_at TEXT NOT NULL
            );
            """)
        
    def setUp(self):
        """Set up test data before each test method."""
        # Create a fresh database for each test
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
        
        # Initialize database with test data
        # Temporarily patch the DB_PATH and db_structure path for testing
        with patch('db.database.DB_PATH', self.test_db), \
             patch('db.database.open', open('/tmp/db_structure', 'r')):
            self.db = Database()
    
    def tearDown(self):
        """Clean up after each test method."""
        self.db._close()
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
    
    def test_add_account_success(self):
        """Test adding a new account successfully."""
        # Arrange
        account_name = "Test Account"
        initial_balance = 1000.0
        
        # Act
        account_id = self.db.add_account(account_name, initial_balance)
        
        # Assert
        self.assertIsNotNone(account_id, "Account ID should not be None")
        
        # Verify the account was actually added to the database
        with sqlite3.connect(self.test_db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM accounts WHERE account_id = ?", (account_id,))
            result = cursor.fetchone()
            
            self.assertIsNotNone(result, "Account should exist in the database")
            self.assertEqual(result[1], account_name, "Account name should match")
            self.assertEqual(result[2], initial_balance, "Initial balance should match")
    
    def test_add_duplicate_account(self):
        """Test adding an account with a duplicate name."""
        # Arrange
        account_name = "Test Account"
        initial_balance = 1000.0
        
        # Add the account once
        first_id = self.db.add_account(account_name, initial_balance)
        self.assertIsNotNone(first_id, "First account should be added successfully")
        
        # Add a different account to ensure the test is working
        second_account = self.db.add_account("Different Account", 500.0)
        self.assertIsNotNone(second_account, "Second different account should be added successfully")
        
        # Act: Try to add account with same name again
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.add_account(account_name, initial_balance)
        
        # Verify only one account exists with the original name
        with sqlite3.connect(self.test_db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM accounts WHERE account_name = ?", (account_name,))
            count = cursor.fetchone()[0]
            self.assertEqual(count, 1, "Should only be one account with this name")

if __name__ == "__main__":
    unittest.main()
