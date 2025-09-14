from config.database import db
from app.models.monitor import Monitor
import datetime
from app.utils.date_utils import parse_custom_date, format_date_to_custom, get_current_date_custom


currency_type = 1
current_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def save_exchange_rate(rates: dict):
    try:
        db.connect(reuse_if_open=True)
        # Extraer fecha_valor del diccionario
        fecha_valor_str = rates.pop('fecha_valor', datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
        
        # Convertir fecha_valor a objeto datetime
        fecha_valor = format_date_valor(fecha_valor_str)
            
        for currency, price in rates.items():
            last_record = get_last_record(currency, 'BCV')
            print(f"Guardando tasa para {currency}: {price} con fecha {fecha_valor}")          
            store_exchange_rate(fecha_valor, last_record, currency, price, last_record.price, currency_type)

        print("✅ Tasas procesadas y validadas en la base de datos.")

    except Exception as e:
        print(f"❌ Error al guardar tasas: {e}")

    finally:
        if not db.is_closed():
            db.close()



def store_exchange_rate(scrapping_date, last_record, currency, price, price_db, currency_type=1):
    if scrapping_date is None:
        print("⚠️ No se pudo guardar la tasa, fecha de scrapping inválida")
        return None
    scrapping_date_str = scrapping_date.strftime('%Y-%m-%d %H:%M:%S')
    last_update_date_db_str = last_record.last_update.strftime('%Y-%m-%d %H:%M:%S') if last_record.last_update else 'None'
    # Si no hay registros previos (last_update_date_db es None), siempre guardar
    # Si hay registros, solo guardar si la fecha de scrapping es mayor
    should_save = (last_record.last_update is None) or (scrapping_date_str > last_update_date_db_str and scrapping_date_str <= current_date)
    print(f"Comparando fechas para {currency}: scrapping_date {scrapping_date_str} vs last_update_date_db {last_update_date_db_str} AND Server Date: {current_date} => should_save: {should_save}")
    if should_save:
        Monitor.create(
                    currency=currency,
                    change=change(price, price_db, last_record.change),
                    color=set_color(price_db, price),
                    image='https://res.cloudinary.com/bcv/image.png',
                    last_update=scrapping_date,
                    last_update_old=last_record.last_update if last_record.last_update else scrapping_date,
                    percent=percent_change(price, price_db),
                    price=float(price),
                    price_old=price_db if price_db else 0.0,
                    symbol=set_symbol(price_db, price),
                    currency_type=currency_type,
                    title='BCV'
                )
        status_msg = "primera vez" if last_record.last_update is None else f"fecha más reciente ({scrapping_date} > {last_record.last_update})"
        print(f"✅ Tasa guardada para {currency}: {price} con fecha {scrapping_date} - {status_msg}")
    else:
        print(f"⚠️ No se guardó la tasa para {currency}, fecha de scrapping {scrapping_date} no es mayor que la última actualización {last_record.last_update}")
        return None


def set_color(present_price, new_price):
    if present_price > new_price:
        return 'red'
    if present_price < new_price:
        return 'green'
    if present_price == new_price:
        return 'gray'
    else:
        return 'gray'

def get_last_record(currency, title):
    try:
        db.connect(reuse_if_open=True)
        last_record = Monitor.select().where(Monitor.currency == currency).where(Monitor.title==title).order_by(Monitor.created_at.desc()).get()
        return last_record
    except Monitor.DoesNotExist:
        # Crear un registro temporal que indica que no hay datos previos
        # last_update=None indica que es la primera vez que se guarda esta moneda
        last_record = Monitor(price=0.0, last_update=None)
        print(f"ℹ️ No hay registros previos para {currency} en {title}")
        return last_record

def percent_change(new_price, old_price):
    if ((old_price is None or old_price is None) or old_price == 0):
        return 0.0  # Evita división por cero
    if new_price is None or new_price == 0:
        return 0.0
    if old_price == new_price:
        return 0.0
    return ((new_price - old_price) / old_price) * 100

def set_symbol(present_price, new_price):
    if present_price is None or new_price is None:
        return '='
    if present_price == new_price:
        return '='
    if new_price > present_price:
        return '▲'
    elif new_price < present_price:
        return '▼'

def format_date_valor(fecha_valor_str):
    """Convierte fecha_valor_str al formato personalizado y luego a datetime"""
    if fecha_valor_str:
        try:
            print(f"Parseando fecha: '{fecha_valor_str}'")
            # Usar utilidades para parsear la fecha
            fecha_dt = parse_custom_date(fecha_valor_str)
            print(f"Usando fecha del BCV: {format_date_to_custom(fecha_dt)}")
            return fecha_dt
        except Exception as e:
            print(f"Error parseando fecha: {e}")
            return datetime.datetime.now()
    else:
        return datetime.datetime.now()
    
    
def change(price, price_db, change_db):
    print(f"Calculando cambio para price: {price}, price_db: {price_db}")
    if price_db is None or price is None:
        print("⚠️ Precio o precio en DB es None, retornando cambio 0.0")
        return 0.0
    if price - price_db == 0.0000:
        print(f"⚠️ Cambio negativo o cero: {price - price_db}, retornando cambio 0.0")
        return change_db
    print(f"✅ Cambio positivo: {price - price_db}")    
    return price - price_db
