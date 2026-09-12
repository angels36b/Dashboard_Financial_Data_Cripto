from multiprocessing import heap

import pandas as pd

df = pd.read_csv('../btcusdt_binance_data.csv')

#we convert the format string to datatime 

df['date'] = pd.to_datetime(df['date']).dt.tz_localize(None)

#ponemos 'date' como indice para usar resample
df = df.set_index('date')

#agregamos a frecuencia diaria con resample

df_daily = df.resample('D').last().reset_index()
print(df_daily.head(5))

#We verific the Gap
date_complet = pd.date_range(
    start=df_daily['date'].min(),
    end=df_daily['date'].max(),
    freq='D'
)

date_incomplet= date_complet.difference(df_daily['date'])
print(f"Dias faltantes: {len(date_incomplet)}")
#save
df_daily.to_csv('data_clean/btcusdt_binance_daily.csv', index=False)


