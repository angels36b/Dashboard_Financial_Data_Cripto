import pandas as pd

# 1. Cargar archivo
df = pd.read_csv('../btcusdt_binance_data.csv')

# step 2. We convert `date` a datetime Sin zona horaria.

df['date'] = pd.to_datetime(df['date'], utc=True).dt.tz_localize(None)

print(df.info())
print(df.head())

# 3 step
df_daily = (
    df.set_index('date')
        .groupby(pd.Grouper(freq='D'))
        .last()
        .reset_index()
)
print("\n--- Date diary ---")
print(df_daily.head())

df_daily.to_csv('data_clean/btcusdt_binance_dayli_clean.csv', index=False)
