import sqlite3
import os
from datetime import datetime

# Define the path to the database file (it will create it if it doesn't exist)
DB_PATH = "app/database/market_data.db"

def get_connection():
    """Creates a connection to the SQLite database."""
    # Ensure the directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db():
    """Creates the necessary tables if they don't exist yet."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create the table for geopolitical and market news
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS geopolitical_news (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source TEXT NOT NULL,
        headline TEXT UNIQUE NOT NULL,
        impact TEXT NOT NULL,
        published_at TEXT NOT NULL,
        scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    # Note: 'headline TEXT UNIQUE' prevents the agent from saving duplicate news!
    
    conn.commit()
    conn.close()
    print(" Database initialized successfully. Table 'geopolitical_news' is ready.")

def save_news(news_list):
    """Saves a list of news dictionaries into the database."""
    conn = get_connection()
    cursor = conn.cursor()
    
    saved_count = 0
    for item in news_list:
        try:
            # INSERT OR IGNORE skips the row if the headline already exists in the DB
            cursor.execute('''
            INSERT OR IGNORE INTO geopolitical_news (source, headline, impact, published_at)
            VALUES (?, ?, ?, ?)
            ''', (item['source'], item['headline'], item['impact'], item['date']))
            
            # Check if a new row was actually inserted (not ignored)
            if cursor.rowcount > 0:
                saved_count += 1
        except Exception as e:
            print(f"❌ Error saving news to DB: {e}")
            
    conn.commit()
    conn.close()
    return saved_count

def init_macro_table():
    """
    We use indicator_name how unique key
    """

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS macro_indicators (
            indicator_name TEXT PRIMARY KEY,
            actual_value REAL,
            forecast_value REAL,
            surprise REAL,
            updated_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_macro_indicators(indicators_list):
    """
    Metod 2: Inyector
    Receives a list of dictionaries with the calculations 
    already made by the agent and injects them into the database
    """
    conn =sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    current_time = datetime.now().strftime("%D %H:%M:%S")

    for item in indicators_list:
        cursor.execute('''
            INSERT OR REPLACE INTO macro_indicators
            (indicator_name, actual_value, forecast_value, surprise, updated_at)
            VALUE (?, ?, ?, ?, ?)
        ''',(
            item['name'],
            item['actual'],
            item['forecast'],
            item['surprise'],
            current_time)
        )
    conn.commit()
    conn.close()
    print(f"BD: {len(indicators_list)} update macro indicators")
# If we run this file directly, just initialize the database
if __name__ == "__main__":
    init_db()