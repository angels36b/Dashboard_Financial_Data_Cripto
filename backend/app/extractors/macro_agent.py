import time

from app.database.db_manager import init_macro_table, save_macro_indicators

def fetch_macro_data_mock():
    """
    SIMULADOR DE API:"""

    return [
        {"name": "CPI", "actual": 3.5, "forecast": 3.4},
        {"name": "FOMC", "actual": 5.50, "forecast": 5.25},
        {"name": "NFP", "actual": 150, "forecast": 175},
        {"name": "ISM_ADP", "actual": 48.5, "forecast": 49.2},
        
    ]

def process_and_save_macro():
    """
    EL CEREBRO DEL AGENTE:
    1. Llama a los datos crudos.
    2. Calcula 'The Surprise' (La desviación).
    3. Envía los datos procesados a la base de datos.
    
    """
    print("Macro Agent: Looking for new market data...")
    #1. Extraer datos crudos
    raw_data = fetch_macro_data_mock()
    processed_data = []

    #mathematic engine
    for item in raw_data:
        surprise_calc = round(item['actual'] - item['forecast'], 2)

        clean_item = {
            "name": item['name'],
            "actual":item['actual'],
            "forecast": item['forecast'],
            "surprise": surprise_calc
        }
        processed_data.append(clean_item)

        print(f"   -> {clean_item['name']}: Salió {clean_item['actual']} | Se esperaba {clean_item['forecast']} | Desviación: {clean_item['surprise']}")
    
    save_macro_indicators(processed_data)

if __name__ == "__main__":
    print("🚀 INICIANDO SISTEMA MACROECONÓMICO...")
    
    # 1. Aseguramos que la tabla exista antes de hacer nada
    init_macro_table()
    
    # 2. Ejecutamos el ciclo una vez para probar
    process_and_save_macro()
    
    print("✅ Prueba del pipeline finalizada.")