
import requests

from app.models.monitor import Monitor

class VesUsdt:
    
    def get_binance_p2p_price(self, trade_type):
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
                "asset": "USDT",
                "fiat": "VES",
                "tradeType": trade_type,
                "page": 1,
                "rows": 1
            }
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            if data['code'] == '000000' and data['data']:
                db = Monitor()
                # Asumiendo que 'data' contiene una lista de anuncios y tomamos el primero
                # Puedes ajustar esto según tus necesidades
                price = data['data'][0]['adv']['price']
                return float(price)
            else:
                print(f"Error en la respuesta de Binance P2P: {data.get('msg', 'No data')}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error al conectar con la API de Binance: {e}")
        return None