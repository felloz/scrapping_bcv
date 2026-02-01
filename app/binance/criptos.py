
import requests

from app.models.monitor import Monitor

class Criptos:
    
    def get_binance_p2p_price(self, trade_type, asset, fiat):
        """
        Realiza una solicitud a la API de Binance P2P y retorna el precio.
        'trade_type' puede ser 'BUY' o 'SELL'.
        """
        try:
            url='https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search'
            headers = {
                'Content-Type': 'application/json'
            }
            
            payload = {
                 "fiat": fiat,
                 "page": 1,
                 "rows": 5,
                 "tradeType": trade_type,
                 "asset": asset,
                 "countries": [],
                 "proMerchantAds": False,
                 "shieldMerchantAds": False,
                 "filterType": "all",
                 "periods": [],
                 "additionalKycVerifyFilter": 0,
                 "ignoreProMerchantAds": True,
                 "publisherType": "merchant",
                 "payTypes": [],
                 "classifies": ["mass", "profession", "fiat_trade"],
                 "tradedWith": False,
                 "followed": False
            }
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            if data['code'] == '000000' and data['data']:
                #db = Monitor()
                # Asumiendo que 'data' contiene una lista de anuncios y tomamos el primero
                # Puedes ajustar esto según tus necesidades
                for ad in data["data"]:
                    if ad.get("privilegeType") == 8:  # Es un anuncio promocionado
                        continue
                    print("Precio mínimo sin promoted:", ad["adv"]["price"])    
                    price = ad["adv"]["price"]
                    return float(price)
            else:
                print(f"Error en la respuesta de Binance P2P: {data.get('msg', 'No data')}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error al conectar con la API de Binance: {e}")
        return None
    
    def get_spot_price(self, currency):
        """
        Obtiene el precio del oro en la moneda especificada.
        Para oro: PAXGUSDT
        """
        try:
            url = f'https://api.binance.com/api/v3/ticker/price?symbol={currency}'
            headers = {
                'Content-Type': 'application/json'}
            response = requests.get(url, headers=headers)
            response.raise_for_status() 
            data = response.json()
            if 'price' in data:
                price = data['price']
                return float(price)
            else:
                print(f"Error en la respuesta de Binance Spot: {data.get('msg', 'No price found')}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error al conectar con la API de Binance Spot: {e}")
               