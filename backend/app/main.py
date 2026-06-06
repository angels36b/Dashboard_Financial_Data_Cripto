from fastapi import FastAPI
from fastapi.middleware.cros import CORSMiddleware
import sqlite3
#1. Create the instance of server
app = FastAPI(title="Solana Data API")

#configurate the middleware to Cors

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #allows any frontend to connect
    allow_credentials=True,
    allow_methods=["*"],
)

DB_PATH = "app/database/market_data.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    #Configurate the format out
    conn.row_factory = sqlite3.Row
    return conn


