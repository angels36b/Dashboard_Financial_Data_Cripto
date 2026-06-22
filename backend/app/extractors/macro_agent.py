import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from app.database.db_manager import init_macro_table, save_macro_indicators

# URL pública oficial de ForexFactory
FOREX_FACTORY_URL = "https://nfs.faireconomy.media/ff_calendar_thisweek.xml"

def fetch_real_macro_data():
    """
    Se conecta a ForexFactory, descarga el calendario de la semana, 
    y extrae los datos económicos reales con escudos contra 'Dirty Data'.
    """
    print("🌐 Conectando a ForexFactory API...")
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(FOREX_FACTORY_URL, headers=headers, timeout=10)
        response.raise_for_status()
       #print("\n--- XML download")
       #print(response.text) #muestra el texto del XML
       #print("----Finish------")


        root = ET.fromstring(response.content)
        processed_data = []
        
        for event in root.findall('event'):
            country_node = event.find('country')
            impact_node = event.find('impact')
            
            country = country_node.text.strip() if country_node is not None and country_node.text else ""
            impact = impact_node.text.strip() if impact_node is not None and impact_node.text else ""
            
            if country == 'USD' and impact == 'High':
                title_node = event.find('title')
                actual_node = event.find('actual')
                forecast_node = event.find('forecast')
                previous_node = event.find('previous')
                date_node = event.find('date') #  Extraemos la fecha del XML
                
                name = title_node.text.strip() if title_node is not None and title_node.text else "Evento Desconocido"
                event_date = date_node.text.strip() if date_node is not None and date_node.text else "Sin Fecha"
                
                actual_str = actual_node.text.strip() if actual_node is not None and actual_node.text else ""
                forecast_str = forecast_node.text.strip() if forecast_node is not None and forecast_node.text else ""
                previous_str = previous_node.text.strip() if previous_node is not None and previous_node.text else ""
                
                if not forecast_str:
                    continue
                
                # FALLBACK logic 
                if actual_str:
                    # El dato 
                    status = "Actual"
                    display_value = actual_str
                    actual_val = clean_number(actual_str)
                    forecast_val = clean_number(forecast_str)
                    surprise = round(actual_val - forecast_val, 2)
                else:
                    # El dato aún no sale, usamos el ANTERIOR
                    status = "After"
                    display_value = previous_str
                    prev_val = clean_number(previous_str)
                    forecast_val = clean_number(forecast_str)
                    surprise = round(prev_val - forecast_val,2)
                
                processed_data.append({
                    "name": name,
                    "actual": display_value, 
                    "forecast": forecast_str,
                    "surprise": surprise,
                    "date": event_date,
                    "status": status
                })
                
        return processed_data

    except Exception as e:
        print(f" Error al obtener datos macro: {e}")
        return []

def clean_number(value_str):
    """
    Convierte textos financieros como "3.4%", "175K", "2.1B" en números flotantes puros.
    """
    if not value_str: return 0.0
    
    clean_str = value_str.replace('%', '').replace(',', '')
    
    multiplier = 1.0
    if 'K' in clean_str:
        multiplier = 1000.0
        clean_str = clean_str.replace('K', '')
    elif 'M' in clean_str:
        multiplier = 1000000.0
        clean_str = clean_str.replace('M', '')
    elif 'B' in clean_str:
        multiplier = 1000000000.0
        clean_str = clean_str.replace('B', '')
        
    try:
        return float(clean_str) * multiplier
    except ValueError:
        return 0.0

def process_and_save_macro():
    print(" Macro Agent: Extrayendo datos reales del mercado...")
    
    real_data = fetch_real_macro_data()
    
    if not real_data:
        print(" No se encontraron datos macroeconómicos de alto impacto publicados esta semana.")
        return

    # Imprimimos en consola para auditoría
    for item in real_data:
         print(f"   -> [{item['date']}] {item['name'][:20]}: {item['actual']} ({item['status']}) | Prev: {item['forecast']} | Desv: {item['surprise']}")
    # Guardamos en la Base de Datos
    save_macro_indicators(real_data)

if __name__ == "__main__":
    print(" INICIANDO SISTEMA MACROECONÓMICO (DATOS REALES)...")
    init_macro_table()
    process_and_save_macro()
    print(" Pipeline de extracción real finalizado.")