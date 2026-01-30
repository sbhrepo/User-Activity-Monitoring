"""Database module for storing messages and user data"""
import sqlite3
from datetime import datetime
from config import MESSAGES_DB

class MessageDatabase:
    def __init__(self):
        self.db_path = MESSAGES_DB
        self.init_db()
    
    def init_db(self):
        """Initialize database with required tables"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sender TEXT NOT NULL,
                    message TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error initializing database: {e}")
    
    def add_message(self, sender, message):
        """Add a message to the database"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO messages (sender, message, timestamp) VALUES (?, ?, ?)',
                (sender, message, datetime.now().isoformat())
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error adding message: {e}")
            return False
    
    def get_messages(self, limit=100):
        """Get recent messages from database"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            cursor.execute(
                'SELECT sender, message, timestamp FROM messages ORDER BY timestamp DESC LIMIT ?',
                (limit,)
            )
            messages = cursor.fetchall()
            conn.close()
            return list(reversed(messages))  # Reverse to show oldest first
        except Exception as e:
            print(f"Error retrieving messages: {e}")
            return []
