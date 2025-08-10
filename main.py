from app.scraping.bcv_scraper import BcvScraper
from app.services.binance_service import save_binance_rate
from app.services.orchestrator import save_exchange_rate
from app.binance.ves_usdt import VesUsdt


def main():
    # Obtener precios de Binance P2P
    print("🔄 Obteniendo precios de Binance P2P...")
    binance = VesUsdt()
    binance_price = binance.get_binance_p2p_price('BUY')
    print(f"💰 Precio de Binance P2P: {binance_price}")
    save_binance_rate(binance_price)

    #Scrapping BCV for exchange rates
    scraper = BcvScraper()
    rates = scraper.get_exchange_rates()
    # Puedes agregar validación o logging aquí si lo deseas
    if rates:
        print(f"🔍 Datos extraídos: {rates}")
        try:
            save_exchange_rate(rates)
            print("Tasas procesadas correctamente.")
        except Exception as e:
            print(f"❌ Error detallado: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("No se pudieron obtener tasas.")

if __name__ == "__main__":
    main()







##############################################################################
# import requests
# from bs4 import BeautifulSoup
# import warnings

# # Suppress SSL warnings
# warnings.filterwarnings('ignore', message='Unverified HTTPS request')

# url = "https://www.bcv.org.ve/"
# headers = {"User-Agent": "Mozilla/5.0"}

# response = requests.get(url, headers=headers, verify=False)
# soup = BeautifulSoup(response.text, "lxml")


# # Method 1: Search for elements containing USD or EUR with numbers
# usd_found = False
# eur_found = False

# # Look for table cells or div elements that might contain rates
# for element in soup.find_all(['td', 'div', 'span']):
#     text = element.get_text(strip=True)
#     if 'USD' in text and any(char.isdigit() for char in text):
#         print(f"USD pattern found: {text}")
#         usd_found = True
#     if 'EUR' in text and any(char.isdigit() for char in text):
#         print(f"EUR pattern found: {text}")
#         eur_found = True

# if not usd_found:
#     print("No USD rate found in table cells/divs")
# if not eur_found:
#     print("No EUR rate found in table cells/divs")

# print("\n" + "-"*50 + "\n")

# # Method 2: Look for common BCV table structure
# tables = soup.find_all('table')
# print(f"Found {len(tables)} tables")

# for i, table in enumerate(tables):
#     rows = table.find_all('tr')
#     print(f"\nTable {i+1} has {len(rows)} rows")
    
#     for j, row in enumerate(rows[:5]):  # Check first 5 rows
#         cells = row.find_all(['td', 'th'])
#         row_text = ' | '.join([cell.get_text(strip=True) for cell in cells])
#         #if ('USD' in row_text or 'EUR' in row_text) and row_text.strip():
#          #   print(f"  Row {j+1}: {row_text}")

# #print("\n" + "-"*50 + "\n")

# # Method 3: Search for specific classes or IDs that might contain rates
# rate_elements = soup.find_all(attrs={'class': lambda x: x and ('rate' in ' '.join(x).lower() 
#                                                                or 'precio' in ' '.join(x).lower() or 'dolar' in ' '.join(x).lower())})
# # if rate_elements:
# #     print("Found elements with rate-related classes:")
# #     for elem in rate_elements[:3]:
# #         print(f"  {elem.get_text(strip=True)}")

# # Method 4: Look for strong, b, or other emphasis tags that might contain rates
# for tag in ['strong', 'b', 'h1', 'h2', 'h3']:
#     elements = soup.find_all(tag)
#     for elem in elements:
#         text = elem.get_text(strip=True)
#         if ('USD' in text or 'EUR' in text) and any(char.isdigit() for char in text):
#             print(f"Found in {tag}: {text}")
