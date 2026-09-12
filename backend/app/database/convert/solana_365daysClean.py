import pandas as pd
import os

df= pd.read_csv('solana_365days.csv')
#create the data column from Dataframe df
#We delete zoneHour utc+1 whit method tz
df['timestamp']=pd.to_datetime(df['timestamp']).dt.tz_localize(None)

df= df.set_index('timestamp')

df_daily=df.resample('D').last().reset_index()

date_complet = pd.date_range(
    start= df_daily['timestamp'].min(),
    end= df_daily['timestamp'].max(),
    freq='D'
)

date_incomplet = date_complet.difference(df_daily['timestamp'])
print(f"Dias faltantes: {len(date_incomplet)}")

print(df_daily.head(5))

df_daily.to_csv('data_clean/solana365_clean.csv', index=False)