import asyncio
import sqlite3
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import db_manager

from app.extractors import whale_agent, news_agent, macro_agent


async def task_whales():
    """Extract data from blockchain every 10 minutes"""
    while True:
        try:

            #Reemplaza 
            await asyncio.to_thread(whale_agent.process_and_save_whales)
        except Exception as e:
            print(f"Error in extract whale {e}")
        await asyncio.sleep(600) #600 segundos = 10 minuts

async def task_news():
    """Extract financy new every 30 minuts"""

    while True:
        try:
            await asyncio.to_thread(news_agent.fetch_and_filter_news)
        except Exception as e:
            print(f"Error in extract of News: {e}")
        await asyncio.sleep(3600) #3600 Secunds = 1 hora.

async def task_macro():
    """Extract indicator macro every 12 hours"""
    while True:
        try:
            # CORRECCIÓN: Llamamos a la función que descarga y GUARDA
            await asyncio.to_thread(macro_agent.process_and_save_macro)
        except Exception as e:
            print(f"Error in extract macroEconomic: {e}")
        await asyncio.sleep(43200) # 43200 segundos = 12 horas


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Asegurar que las tablas existan AL INICIAR
    db_manager.init_db()
    db_manager.init_macro_table()
    db_manager.init_whale_table()
    # AL INICIAR DOCKER: Arrancamos los temporizadores
    t_whales = asyncio.create_task(task_whales())
    t_news = asyncio.create_task(task_news())
    t_macro = asyncio.create_task(task_macro())
    
    yield # La API comienza a escuchar peticiones aquí
    
    # AL APAGAR DOCKER: Cancelamos los temporizadores de forma segura
    t_whales.cancel()
    t_news.cancel()
    t_macro.cancel()

#1. Create the instance of server, your name is App

app = FastAPI(title="Solana Data API", lifespan=lifespan)
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

### ENDPOINTS DE LA API (RUTAS)
@app.get("/")
def read_root():
    """
    Rute path (health check). confirm that the API is alive
    """
    return{
        "status": "online",
        "message": "добро пожаловать",
        "data_endpoint": "/api/news"
    }

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

        
@app.get("/api/macro")
def get_macro_indicators():
    """
    Extrae los indicadores macro de la base de datos, incluyendo fechas y estado.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # ACTUALIZAMOS: Pedimos las nuevas columnas event_date y status
        cursor.execute("""
            SELECT indicator_name, actual_value, forecast_value, surprise, event_date, status 
            FROM macro_indicators 
            ORDER BY event_date ASC, indicator_name ASC
        """)
        rows = cursor.fetchall()
        conn.close()
        
        macro_data = [dict(row) for row in rows]
        return {"status": "success", "data": macro_data}
        
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/whales")
def get_whale_flows():
    """
    Extrae los flujos institucionales de la base de datos
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
 
        cursor.execute(
        """
            SELECT direction, amount, exchange, timestamp
            FROM whale_flows
            ORDER BY timestamp DESC
            LIMIT 10
        """
        )
        rows = cursor.fetchall()
        conn.close()

        whale_data = [dict(row) for row in rows]
        return {"status": "success", "data": whale_data}
    
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
