import time 
from app.database.db_manager import init_whale_table, save_whale_flows

def fetch_whale_data_mock():
    """
    simulador
    """
    return [
        {"direction": "Long", "amount": 850.5, "exchange":"Binance"},
        {"direction": "Short", "amount": 1200.0, "exchange": "coinbase"},
        {"direction": "Transfer", "amount": 5000.0, "exchange": "Unknown Wallet -> Kraken"}
    ]

def process_and_save_whaless():
    print("whale Agent: Escaneando transacciones institucionales.")
    raw_data = fetch_whale_data_mock()

    for item in raw_data:
        print(f"Alerta ballena:{item['direction']} de {item['amount']} BTC en {item['exchange']}")
    save_whale_flows(raw_data)

if __name__ == "__main__":
    print("Iniciando Rastreador en order flow (Whales)...")
    init_whale_table()
    process_and_save_whaless()
    print("Flujo institucional registrado.")