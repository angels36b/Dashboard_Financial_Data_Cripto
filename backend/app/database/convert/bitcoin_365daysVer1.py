import pandas as pd

# 1. load file
df = pd.read_csv('bitcoin_365days.csv')

# 2. to Convert timestamp to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'], format='%d/%m/%Y %H:%M')

# 3. Comprobar días faltantes (solo informativo)
fechas_completas = pd.date_range(start=df['timestamp'].min(), 
                                 end=df['timestamp'].max(), 
                                 freq='D')
fechas_faltantes = fechas_completas.difference(df['timestamp'])
print(f"Días faltantes: {len(fechas_faltantes)}")

# 4. Guardar el archivo con el cambio aplicado
df.to_csv('bitcoin_365days_clean.csv', index=False)

print("✅ Archivo guardado como 'bitcoin_365days_clean.csv'")