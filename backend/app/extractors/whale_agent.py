import requests
from datetime import datetime
from app.database.db_manager import init_whale_table, save_whale_flows

# Usamos la API pública y gratuita del explorador de bloques de Bitcoin
BLOCKCHAIN_API_URL = "https://blockchain.info/unconfirmed-transactions?format=json"
WHALE_THRESHOLD_BTC = 0.5  # 15 BTC = Aprox $1,000,000 USD

def fetch_free_onchain_whales():
    """
    Se conecta directamente a la Blockchain de Bitcoin, sin API Keys,
    y filtra transacciones masivas en tiempo real extrayendo el Hash de origen.
    """
    print("🌐 Conectando a la Blockchain pública de Bitcoin (Mempool)...")
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(BLOCKCHAIN_API_URL, headers=headers, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        transactions = data.get('txs', [])
        whale_orders = []
        
        for tx in transactions:
            # 1. Sumamos los Satoshis y convertimos a BTC
            total_sats = sum(out.get('value', 0) for out in tx.get('out', []))
            amount_btc = total_sats / 100_000_000
            
            # 2. Filtro Institucional
            if amount_btc >= WHALE_THRESHOLD_BTC:
                direction = "Transfer"
                inputs = tx.get('inputs', [])
                from_address = "Desconocida"
                
                # 3. Extracción de la billetera criptográfica
                if inputs and 'prev_out' in inputs[0] and 'addr' in inputs[0]['prev_out']:
                    from_address = inputs[0]['prev_out']['addr']
                
                # 4. Formateo visual
                if from_address != "Desconocida":
                    short_wallet = f"{from_address[:6]}...{from_address[-4:]}"
                    exchange_display = f"Desde: {short_wallet}"
                else:
                    exchange_display = "Red On-Chain (Oculta)"
                
                trade_time = datetime.fromtimestamp(tx['time']).strftime('%Y-%m-%d %H:%M:%S')
                
                #LA LÍNEA CRÍTICA QUE FALTABA: Agregar el diccionario a la lista
                whale_orders.append({
                    "direction": direction,
                    "amount": round(amount_btc, 2),
                    "exchange": exchange_display,
                    "timestamp": trade_time
                })
                
        # 5. Ordenar por cantidad y retornar
        whale_orders = sorted(whale_orders, key=lambda x: x['amount'], reverse=True)[:10]
        return whale_orders

    except Exception as e:
        print(f" Error al obtener datos de la Blockchain: {e}")
        return []

def process_and_save_whales():
    print("Whale Agent: Escaneando la red Bitcoin en busca de transferencias masivas...")
    
    real_data = fetch_free_onchain_whales()
    
    if not real_data:
        print(f" El mercado está tranquilo. No hay transacciones > {WHALE_THRESHOLD_BTC} BTC ahora mismo.")
        return
        
    for item in real_data:
        print(f"   {item['direction'].upper()} | {item['amount']} BTC | {item['exchange']}")
        
    # Inyectamos a la base de datos
    save_whale_flows(real_data)

if __name__ == "__main__":
    print(" INICIANDO RASTREADOR DE ORDER FLOW (100% GRATIS)...")
    init_whale_table()
    process_and_save_whales()
    print("✅ Escaneo On-Chain finalizado.")