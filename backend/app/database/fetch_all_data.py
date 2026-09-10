import requests
import pandas as pd
from datetime import datetime, timedelta
import time

# ============================================
# CONFIGURACIÓN
# ============================================
SYMBOLS = ["BTCUSDT", "SOLUSDT"]
LIMIT = 500  # Número de registros a descargar

# ============================================
# FUNCIONES PARA DESCARGAR DATOS
# ============================================

def fetch_funding_rate(symbol, limit=500):
    """
    Descarga el histórico de Funding Rate desde Binance Futures.
    Devuelve DataFrame con columnas: date, funding_rate
    """
    url = "https://fapi.binance.com/fapi/v1/fundingRate"
    params = {
        "symbol": symbol,
        "limit": limit
    }
    
    print(f"📥 Descargando Funding Rate para {symbol}...")
    
    try:
        response = requests.get(url, params=params, timeout=30)
        
        if response.status_code != 200:
            print(f"❌ Error HTTP {response.status_code}: {response.text[:200]}")
            return pd.DataFrame()
        
        data = response.json()
        
        if not data:
            print(f"⚠️ No hay datos de Funding Rate para {symbol}")
            return pd.DataFrame()
        
        # Crear DataFrame
        df = pd.DataFrame(data)
        
        # Convertir timestamp a datetime
        df['date'] = pd.to_datetime(df['fundingTime'], unit='ms', utc=True)
        
        # Convertir funding rate a número
        df['funding_rate'] = pd.to_numeric(df['fundingRate'], errors='coerce')
        
        # Seleccionar columnas
        df = df[['date', 'funding_rate']]
        df = df.dropna()
        df = df.sort_values('date')
        
        print(f"✅ {len(df)} registros de Funding Rate para {symbol}")
        return df
        
    except Exception as e:
        print(f"❌ Error descargando Funding Rate de {symbol}: {e}")
        return pd.DataFrame()


def fetch_open_interest_hist(symbol, period="1h", limit=500):
    """
    Descarga el histórico de Open Interest desde Binance Futures Data.
    Devuelve DataFrame con columnas: date, open_interest
    """
    url = "https://fapi.binance.com/futures/data/openInterestHist"
    params = {
        "symbol": symbol,
        "period": period,  # '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d'
        "limit": limit
    }
    
    print(f"📥 Descargando Open Interest para {symbol}...")
    
    try:
        response = requests.get(url, params=params, timeout=30)
        
        if response.status_code != 200:
            print(f"❌ Error HTTP {response.status_code}: {response.text[:200]}")
            return pd.DataFrame()
        
        data = response.json()
        
        if not data:
            print(f"⚠️ No hay datos de Open Interest para {symbol}")
            return pd.DataFrame()
        
        # Crear DataFrame
        df = pd.DataFrame(data)
        
        # Convertir timestamp a datetime
        df['date'] = pd.to_datetime(df['timestamp'], unit='ms', utc=True)
        
        # Convertir open interest a número
        df['open_interest'] = pd.to_numeric(df['sumOpenInterest'], errors='coerce')
        
        # Seleccionar columnas
        df = df[['date', 'open_interest']]
        df = df.dropna()
        df = df.sort_values('date')
        
        print(f"✅ {len(df)} registros de Open Interest para {symbol}")
        return df
        
    except Exception as e:
        print(f"❌ Error descargando Open Interest de {symbol}: {e}")
        return pd.DataFrame()


def fetch_current_price(symbol):
    """
    Obtiene el precio actual del símbolo desde Binance Futures.
    """
    url = "https://fapi.binance.com/fapi/v1/ticker/price"
    params = {"symbol": symbol}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        return float(data['price'])
    except:
        return None


def fetch_current_oi(symbol):
    """
    Obtiene el Open Interest actual del símbolo desde Binance Futures.
    """
    url = "https://fapi.binance.com/fapi/v1/openInterest"
    params = {"symbol": symbol}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        return float(data['openInterest'])
    except:
        return None


def combinar_datos(df_oi, df_fr):
    """
    Combina Open Interest y Funding Rate por fecha.
    Usa merge_asof para alinear los timestamps más cercanos.
    """
    if df_oi.empty or df_fr.empty:
        print("❌ No se pueden combinar datos vacíos")
        return pd.DataFrame()
    
    # Ordenar por fecha
    df_oi = df_oi.sort_values('date')
    df_fr = df_fr.sort_values('date')
    
    # Combinar usando merge_asof (encuentra el valor más cercano en el tiempo)
    df_combinado = pd.merge_asof(
        df_oi,
        df_fr,
        on='date',
        direction='nearest'
    )
    
    return df_combinado


def descargar_todo(symbol):
    """
    Descarga todos los datos para un símbolo y los combina.
    """
    print(f"\n{'='*60}")
    print(f"🚀 PROCESANDO {symbol}")
    print('='*60)
    
    # 1. Descargar Funding Rate
    df_fr = fetch_funding_rate(symbol, LIMIT)
    
    # 2. Descargar Open Interest
    df_oi = fetch_open_interest_hist(symbol, period="1h", limit=LIMIT)
    
    # 3. Verificar que hay datos
    if df_fr.empty:
        print(f"❌ No se pudo descargar Funding Rate para {symbol}")
        return pd.DataFrame()
    
    if df_oi.empty:
        print(f"❌ No se pudo descargar Open Interest para {symbol}")
        return pd.DataFrame()
    
    # 4. Combinar datos
    df_combinado = combinar_datos(df_oi, df_fr)
    
    if df_combinado.empty:
        print(f"❌ No se pudieron combinar los datos para {symbol}")
        return pd.DataFrame()
    
    # 5. Obtener datos actuales para referencia
    precio_actual = fetch_current_price(symbol)
    oi_actual = fetch_current_oi(symbol)
    
    # 6. Guardar a CSV
    filename = f"{symbol.lower()}_binance_data.csv"
    df_combinado.to_csv(filename, index=False)
    
    # 7. Mostrar resumen
    print(f"\n📊 Resumen de {symbol}:")
    print(f"   Rango de fechas: {df_combinado['date'].min()} a {df_combinado['date'].max()}")
    print(f"   Total registros: {len(df_combinado)}")
    print(f"   Último funding rate: {df_combinado['funding_rate'].iloc[-1]:.6f}")
    print(f"   Último open interest: {df_combinado['open_interest'].iloc[-1]:,.0f}")
    if precio_actual:
        print(f"   Precio actual: ${precio_actual:,.2f}")
    if oi_actual:
        print(f"   Open Interest actual: ${oi_actual:,.0f}")
    
    print(f"💾 Datos guardados en: {filename}")
    
    return df_combinado


# ============================================
# EJECUCIÓN PRINCIPAL
# ============================================

if __name__ == "__main__":
    print("="*60)
    print("🚀 DESCARGANDO DATOS DESDE BINANCE FUTURES")
    print("="*60)
    print(f"📊 Símbolos a descargar: {SYMBOLS}")
    print(f"📈 Límite de registros: {LIMIT}")
    print("="*60)
    
    resultados = {}
    
    for symbol in SYMBOLS:
        df = descargar_todo(symbol)
        resultados[symbol] = df
        
        # Pequeña pausa para no saturar la API
        time.sleep(1)
    
    # ============================================
    # RESUMEN FINAL
    # ============================================
    print("\n" + "="*60)
    print("✅ ¡PROCESO COMPLETADO!")
    print("="*60)
    
    for symbol, df in resultados.items():
        if not df.empty:
            print(f"📁 {symbol}: {symbol.lower()}_binance_data.csv ({len(df)} registros)")
            print(f"   Últimos 3 registros:")
            print(df.tail(3).to_string(index=False))
            print()
        else:
            print(f"❌ {symbol}: No se descargaron datos")
    
    print("\n💡 Archivos generados:")
    for symbol in SYMBOLS:
        print(f"   - {symbol.lower()}_binance_data.csv")
    
    print("\n🎯 Datos disponibles en los CSV:")
    print("   - date: Fecha y hora (UTC)")
    print("   - open_interest: Interés abierto en USD")
    print("   - funding_rate: Tasa de financiación (último valor)")