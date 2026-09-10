import requests
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
import os

# Cargar .env
load_dotenv(Path(__file__).parent.parent.parent / '.env')
FRED_API_KEY = os.getenv('FRED_API_KEY')

def descargar_fred(serie_id, nombre):
    url = "https://api.stlouisfed.org/fred/series/observations"
    
    # ✅ frequency = 'd' (NO 'daily')
    params = {
        'series_id': serie_id,
        'api_key': FRED_API_KEY,
        'file_type': 'json',
        'observation_start': '2020-01-01',
        'frequency': 'd',  # ← CAMBIADO: 'd' en lugar de 'daily'
        'limit': 100000
    }
    
    print(f"📥 Descargando {nombre}...")
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        print(f"❌ Error {response.status_code}: {response.text[:200]}")
        return pd.DataFrame()
    
    data = response.json()
    
    if 'observations' not in data:
        print(f"❌ No se encontraron datos")
        return pd.DataFrame()
    
    df = pd.DataFrame(data['observations'])
    df['date'] = pd.to_datetime(df['date'])
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    df = df.dropna()[['date', 'value']]
    df.columns = ['date', nombre]
    
    print(f"✅ {nombre}: {len(df)} registros")
    return df

if __name__ == "__main__":
    # Descargar VIX
    df_vix = descargar_fred('VIXCLS', 'VIX')
    if not df_vix.empty:
        df_vix.to_csv('vix_data.csv', index=False)
        print(f"💾 Guardado: vix_data.csv")
        print(df_vix.tail())
    
    # Descargar DXY
    df_dxy = descargar_fred('DTWEXBGS', 'DXY')
    if not df_dxy.empty:
        df_dxy.to_csv('dxy_data.csv', index=False)
        print(f"💾 Guardado: dxy_data.csv")
        print(df_dxy.tail())