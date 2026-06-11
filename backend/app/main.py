from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
#1. Create the instance of server, your name is App
app = FastAPI(title="Solana Data API")

#configurate the middleware to Cors
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, #allows any frontend to connect
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers = ["Authorization", "Content-Type"],
)

DB_PATH = "app/database/market_data.db"


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    #Configurate the format out
    conn.row_factory = sqlite3.Row
    return conn


@app.get("/api/news")
def get_latest_news():
    """
    extract the last 10 news from the database
    """
    try: 
        conn = get_db_connection()
        cursor = conn.cursor()

        #Consulta SQL: bring everything from the table, sorted from the newest to the oldest
        cursor.execute('''
        SELECT source, headline, impact, published_at
        FROM geopolitical_news
        ORDER BY id DESC
        LIMIT 10
        ''')
        rows = cursor.fetchall()
        conn.close()

        #we convert the sql ROWS IN THE LIST OF PYTHON DICTIONARY
        news_list = [dict(row) for row in rows]
        return {"status": "success", "data": news_list}
    
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
def read_root():
    """
    Rute path (health check). confirm that the API is alive
    """
    return{
        "status": "online",
        "message": "добро пожаловать",
        "data_endpoint": "/api/news"
    }
        
@app.get("/api/macro")
def get_macro_indicators():
    """
    Extrae los indicadores macro de la base de datos
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        #pedimos los datos
        cursor.execute(
        """
        SELECT indicator_name, actual_value, forecast_value, surprise, updated_at
        FROM macro_indicators
        ORDER BY indicator_name 
        """
        )
        rows = cursor.fetchall()
        conn.close()

        #empaquetamos todo en una lista de diccionarios JSON
        macro_data = [dict(row) for row in rows]
        #Enviamos la respuesta exitosa
        return {"status": "success", "data": macro_data}
    
    except Exception as e:
        #Si algo falla en la BD, lo informamos al frontEnd
        return {"status": "error", "message":str(e)}
