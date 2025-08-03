import requests
from bs4 import BeautifulSoup
import warnings
import re
from urllib3.exceptions import InsecureRequestWarning
import datetime

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
            
            # Buscar fecha valor con patrón específico del BCV
            date_patterns = [
                r"Fecha Valor[:\s]*([A-Za-z]+,\s*[0-9]{1,2}\s+[A-Za-z]+\s+[0-9]{4})",
                r"Fecha Valor[:\s]*([0-9]{1,2}\s+[A-Za-z]+\s+[0-9]{4})",
                r"Fecha Valor[:\s]*([0-9]{1,2}/[0-9]{1,2}/[0-9]{4})",
                r"([A-Za-z]+,\s*[0-9]{1,2}\s+[A-Za-z]+\s+[0-9]{4})"
            ]
            
            fecha_valor = None
            fecha_str = None
            
            for pattern in date_patterns:
                date_match = re.search(pattern, content, re.IGNORECASE)
                if date_match:
                    fecha_str = date_match.group(1)
                    print(f"📅 Fecha encontrada: {fecha_str}")
                    break
            
            # Procesar la fecha encontrada
            if fecha_str:
                try:
                    # Mapeo de meses en español a números
                    meses_spanish = {
                        'enero': '01', 'febrero': '02', 'marzo': '03', 'abril': '04',
                        'mayo': '05', 'junio': '06', 'julio': '07', 'agosto': '08',
                        'septiembre': '09', 'octubre': '10', 'noviembre': '11', 'diciembre': '12'
                    }
                    
                    # Limpiar la fecha (remover día de la semana y comas)
                    fecha_limpia = re.sub(r'^[A-Za-z]+,\s*', '', fecha_str)  # Remover "Lunes, "
                    
                    # Extraer día, mes y año usando regex
                    match = re.match(r'([0-9]{1,2})\s+([A-Za-z]+)\s+([0-9]{4})', fecha_limpia)
                    
                    if match:
                        dia = match.group(1).zfill(2)  # Añadir cero si es necesario
                        mes_texto = match.group(2).lower()
                        anio = match.group(3)
                        
                        # Convertir mes de texto a número
                        mes_num = meses_spanish.get(mes_texto)
                        
                        if mes_num:
                            fecha_valor = f"{anio}-{mes_num}-{dia} 12:00"
                            print(f"✅ Fecha parseada correctamente: {fecha_valor}")
                        else:
                            print(f"⚠️ Mes no reconocido: {mes_texto}")
                            fecha_valor = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                    else:
                        print(f"⚠️ Formato de fecha no reconocido: {fecha_limpia}")
                        fecha_valor = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                            
                    if not fecha_valor:
                        print(f"⚠️ No se pudo parsear la fecha {fecha_str}, usando fecha actual")
                        fecha_valor = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                        
                except Exception as e:
                    print(f"⚠️ Error procesando fecha: {e}")
                    fecha_valor = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            else:
                print("⚠️ No se encontró fecha valor, usando fecha actual")
                fecha_valor = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            
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
