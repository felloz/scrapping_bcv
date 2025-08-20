import requests
from bs4 import BeautifulSoup
import warnings
import re
from urllib3.exceptions import InsecureRequestWarning
import datetime
from app.utils.date_utils import parse_bcv_date, get_current_date_custom

# Suppress SSL warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

class BcvScraper:
    def __init__(self):
        self.url = "https://www.bcv.org.ve/"
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

    def get_exchange_rates(self):
        try:
            response = requests.get(self.url, headers=self.headers, verify=False)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            content = soup.get_text()

            # Buscar tasas de cambio
            usd_match = re.search(r"USD\s*([0-9.,]+)", content)
            eur_match = re.search(r"EUR\s*([0-9.,]+)", content)
            
            # Buscar fecha valor específicamente del BCV
            # Usar un patrón más flexible que capture todo hasta el año
            fecha_valor_pattern = r"Fecha Valor[:\s]*(.*\d{4})"
            fecha_valor_match = re.search(fecha_valor_pattern, content, re.IGNORECASE)
            
            
            fecha_valor = None
            fecha_str = None
            
            if fecha_valor_match:
                fecha_str = fecha_valor_match.group(1)
                print(f"📅 Fecha Valor encontrada: {fecha_str}")
            else:
                # Fallback: buscar otros patrones solo si no se encuentra "Fecha Valor"
                fallback_patterns = [
                    r"Fecha Valor[:\s]*([0-9]{1,2}\s+[A-Za-z]+\s+[0-9]{4})",
                    r"Fecha Valor[:\s]*([0-9]{1,2}/[0-9]{1,2}/[0-9]{4})"
                ]
                
                for pattern in fallback_patterns:
                    date_match = re.search(pattern, content, re.IGNORECASE)
                    if date_match:
                        fecha_str = date_match.group(1)
                        print(f"📅 Fecha encontrada (fallback): {fecha_str}")
                        break
            
            # Procesar la fecha encontrada usando utilidades
            if fecha_str:
                fecha_valor = parse_bcv_date(fecha_str)
                print(f"✅ Fecha parseada: {fecha_valor}")
            else:
                print("⚠️ No se encontró fecha valor, usando fecha actual")
                fecha_valor = get_current_date_custom()
            
            if not usd_match or not eur_match:
                print("Could not find exchange rates on the page.")
                return None

            usd = usd_match.group(1)
            eur = eur_match.group(1)
            return { 
                "USD": float(usd.replace(",", ".")),
                "EUR": float(eur.replace(",", ".")),
                "fecha_valor": fecha_valor
            }

        except Exception as e:
            print(f"Error en scraping BCV: {e}")
            return None
