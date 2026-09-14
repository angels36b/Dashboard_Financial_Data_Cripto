import yfinance as yf
import pandas as pd

def get_5_years_yf(symbol, coin_name):
    # Descargar 5 años de datos diarios
    df = yf.download(symbol, period="5y", interval="1d")
    
    # Limpiar y renombrar columnas
    df = df.reset_index()
    df = df.rename(columns={"Date": "date", "Close": "price"})
    df["coin"] = coin_name
    
    return df[["date", "price", "coin"]]

# --- Descargar Solana y Bitcoin ---
df_sol = get_5_years_yf("SOL-USD", "solana")
df_btc = get_5_years_yf("BTC-USD", "bitcoin")

# --- Unir ambas monedas ---
df_final = pd.concat([df_sol, df_btc], ignore_index=True)

print(df_final.head())
print(df_final.tail())
print(df_final["coin"].value_counts())

df_final.to_csv("convert/data_clean/solANDbtc.csv")