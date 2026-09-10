from pycoingecko import CoinGeckoAPI
import pandas as pd

cg = CoinGeckoAPI()

def descargar_coingecko(coin_id, vs_currency='usd', days=365):
    """Descarga datos desde CoinGecko"""
    
    print(f"Descargando {coin_id}...")
    
    # Obtener datos históricos
    data = cg.get_coin_market_chart_by_id(
        id=coin_id,
        vs_currency=vs_currency,
        days=days
    )
    
    # Crear DataFrame
    df = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    
    # Guardar
    filename = f"{coin_id}_{days}days.csv"
    df.to_csv(filename)
    print(f"✅ Guardado: {filename}")
    
    return df

# Descargar
btc = descargar_coingecko('bitcoin', days=365)
sol = descargar_coingecko('solana', days=365)