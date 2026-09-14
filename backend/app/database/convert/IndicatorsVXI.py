import yfinance as yf
import requests
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
import os

# ==========================================
# CONFIGURACIÓN INICIAL
# ==========================================
# Carga las variables de entorno (incluida tu FRED_API_KEY) desde el archivo .env
load_dotenv(Path(__file__).parent.parent.parent / '.env')
FRED_API_KEY = os.getenv('FRED_API_KEY')

# Define la fecha de inicio que coincide con tus datos de BTC y Solana
FECHA_INICIO = '2021-09-12'

# ==========================================
# FUNCIÓN PARA DESCARGAR DATOS DE FRED (para el VIX)
# ==========================================
def descargar_fred(serie_id, nombre, fecha_inicio):
    """
    Descarga una serie temporal desde la API de FRED.
    
    Parámetros:
    - serie_id: El ID de la serie en FRED (ej. 'VIXCLS')
    - nombre: El nombre que tendrá la columna en el DataFrame final
    - fecha_inicio: Fecha desde la cual empezar a descargar (formato 'YYYY-MM-DD')
    """
    url = "https://api.stlouisfed.org/fred/series/observations"
    
    params = {
        'series_id': serie_id,
        'api_key': FRED_API_KEY,
        'file_type': 'json',
        'observation_start': fecha_inicio,  # ✅ Alineado con tus datos de cripto
        'frequency': 'd',                   # ✅ Frecuencia diaria
        'limit': 100000
    }
    
    print(f"📥 Descargando {nombre} desde FRED...")
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        print(f"❌ Error {response.status_code}: {response.text[:200]}")
        return pd.DataFrame()
    
    data = response.json()
    
    if 'observations' not in data:
        print(f"❌ No se encontraron datos para {nombre}")
        return pd.DataFrame()
    
    # Crea un DataFrame con los datos y limpia los tipos
    df = pd.DataFrame(data['observations'])
    df['date'] = pd.to_datetime(df['date'])
    df['value'] = pd.to_numeric(df['value'], errors='coerce') # Convierte '.' a NaN
    df = df.dropna()[['date', 'value']]  # Elimina filas con valores faltantes
    df.columns = ['date', nombre]        # Renombra la columna de valor
    
    print(f"✅ {nombre}: {len(df)} registros descargados.")
    return df

# ==========================================
# DESCARGA DEL DXY CLÁSICO (usando yfinance)
# ==========================================
def descargar_dxy_clasico(fecha_inicio):
    """
    Descarga el DXY clásico desde Yahoo Finance usando el ticker 'DX-Y.NYB'.
    """
    print("📥 Descargando DXY clásico desde Yahoo Finance...")
    
    try:
        # Descarga los datos. El ticker 'DX-Y.NYB' es el del DXY clásico.
        dxy_data = yf.download('DX-Y.NYB', start=fecha_inicio, progress=False)
        
        # Verifica si se descargaron datos
        if dxy_data.empty:
            print("❌ No se pudieron obtener datos del DXY desde Yahoo Finance.")
            return pd.DataFrame()
        
        # Prepara el DataFrame: resetea el índice para tener 'Date' como columna
        df_dxy = dxy_data.reset_index()
        
        # Selecciona y renombra las columnas que nos interesan
        # Usamos 'Close' como el valor diario del DXY
        df_dxy = df_dxy[['Date', 'Close']]
        df_dxy.columns = ['date', 'DXY']
        
        # Asegura que la columna 'date' sea de tipo datetime sin zona horaria
        df_dxy['date'] = pd.to_datetime(df_dxy['date']).dt.tz_localize(None)
        
        print(f"✅ DXY: {len(df_dxy)} registros descargados.")
        return df_dxy
        
    except Exception as e:
        print(f"❌ Error al descargar DXY: {e}")
        return pd.DataFrame()

# ==========================================
# BLOQUE PRINCIPAL DE EJECUCIÓN
# ==========================================
if __name__ == "__main__":
    
    # 1. Descargar el VIX desde FRED
    df_vix = descargar_fred('VIXCLS', 'VIX', FECHA_INICIO)
    
    # 2. Descargar el DXY clásico desde Yahoo Finance
    df_dxy = descargar_dxy_clasico(FECHA_INICIO)
    
    # 3. Guardar los archivos individualmente (opcional, pero útil)
    if not df_vix.empty:
        df_vix.to_csv('vix_data.csv', index=False)
        print(f"💾 Guardado: vix_data.csv")
    
    if not df_dxy.empty:
        df_dxy.to_csv('dxy_data.csv', index=False)
        print(f"💾 Guardado: dxy_data.csv")
    
    # 4. (Opcional) Unir ambos en un solo DataFrame para tenerlos juntos
    # Esto es útil si vas a hacer un merge posterior con tus datos de cripto.
    if not df_vix.empty and not df_dxy.empty:
        # Unimos por la columna 'date' usando un 'outer join' para no perder datos
        df_macro = pd.merge(df_dxy, df_vix, on='date', how='outer')
        # Rellenamos posibles huecos (fines de semana, festivos) con el valor anterior
        df_macro = df_macro.sort_values('date').ffill()
        df_macro.to_csv('macro_data.csv', index=False)
        print(f"💾 Guardado: macro_data.csv (DXY y VIX unidos)")
        print(df_macro.head())