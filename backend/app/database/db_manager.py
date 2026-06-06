import sqlite3
import os

#define the path to the database file (it will create it if it doesnt exist)
DB_PATH = "app/database/market_data.db"

def get_connection():
    """creates a connection to the SQLite database"""

    #Ensure the directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db():
    """Creates the necessary tables if they don't exist yet."""
    conn = get_connection()
    cursor = conn.cursor()

    #Create the table for geopolitical and market news

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS geopolitical_news (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   source TEXT NOT NULL,
                   headline TEXT UNIQUE NOT NULL,
                   impact TEXT NOT NULL,
                   scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
''')
    conn.commit()
    conn.close()
    print("Database initialized successfully")

    def save_news(news_list):
        """Saves a list of news dictionaries into the database"""
        conn = get_connection()
        cursor = conn.cursor()

        saved_count = 0
        for item in news_list:
            try:
                #INSERT PR IGNORE skips the row if the headline already exists in the DB
                cursor.execute('''
                INSERT OR IGNORE INTO geopolitical_news(source, headline, impact, published_at)
                VALUES(?,?,?)
                ''',(item['source'], item['headline'], item['impact'], item['date']))

                #Check ir a new row was actually inserted
                if cursor.rowcount > 0:
                    saved_count += 1
            except Exception as e:
                print(f"Error saving news to DB: {e}")
        
        conn.commit()
        conn.close()
        return saved_count
    #if we run this file directly, just initialize the database
    if __name__ == "__main__":
        init_db()