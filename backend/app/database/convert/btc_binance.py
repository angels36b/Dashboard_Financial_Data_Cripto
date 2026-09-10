import pandas as pd

# 1. Cargar archivo
df = pd.read_csv('../btcusdt_binance_data.csv')

# 2. Convertir a datetime y eliminar zona horaria (+00:00)
df['date'] = pd.to_datetime(df['date']).dt.tz_localize(None)

print(df.info())
print(df.head())

# 3. Agregar a frecuencia diaria (tomamos el ÚLTIMO valor del día = cierre a las 23:00)
# Extraemos la fecha sin hora para agrupar
df_daily = df.groupby(df['date'].dt.date).last().reset_index(drop=False)
# Renombramos la columna 'date' (que ahora es la fecha sin hora) a 'date'
df_daily.rename(columns={'date': 'date'}, inplace=True)
# Convertimos la columna 'date' a datetime para que sea compatible con los otros archivos
df_daily['date'] = pd.to_datetime(df_daily['date'])

# Mostrar resultado
print("\n--- Datos diarios (último valor del día) ---")
print(df_daily.head())

# 4. Guardar el archivo limpio
df_daily.to_csv('btcusdt_binance_daily.csv', index=False)
print("\n✅ Archivo guardado como 'btcusdt_binance_daily.csv'")