from config.database import db
from app.models.monitor import Monitor
import datetime

def save_exchange_rate(rates: dict):
    try:
        db.connect(reuse_if_open=True)
        # Extraer fecha_valor del diccionario
        fecha_valor_str = rates.pop('fecha_valor', datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
        
        # Convertir fecha_valor a objeto datetime
        fecha_valor = format_date_valor(fecha_valor_str)
            
        for currency, price in rates.items():
            last_record = get_last_record(currency)          
            Monitor.create(
                type='bcv',
                change=price - last_record.price if last_record else 0.0,  # Puedes calcularlo si tienes datos anteriores
                color=set_color(last_record.price, price),
                image='https://res.cloudinary.com/bcv/image.png',
                last_update=fecha_valor,
                last_update_old=last_record.last_update if last_record else datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
                percent=percent_change(price, last_record.price == 0.0),
                price=float(price),
                price_old=last_record.price if last_record else 0.0,  # Temporal, hasta que calcules diferencia
                symbol=set_symbol(last_record.price, price),
                title=currency
            )

        print("✅ Tasas guardadas en la base de datos.")

    except Exception as e:
        print(f"❌ Error al guardar tasas: {e}")

    finally:
        if not db.is_closed():
            db.close()


def set_color(present_price, new_price):
    if present_price > new_price:
        return 'red'
    if present_price < new_price:
        return 'green'
    if present_price == new_price:
        return 'gray'
    else:
        return 'gray'

def get_last_record(currency):
    try:
        db.connect(reuse_if_open=True)
        last_record = Monitor.select().where(Monitor.title == currency).order_by(Monitor.created_at.desc()).get()
        return last_record
    except Monitor.DoesNotExist:
        last_record = Monitor(price=0.0, last_update=datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
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
    if fecha_valor_str:
            try:
                # Limpiar la cadena de fecha
                fecha_limpia = fecha_valor_str.strip()
                print(f"Parseando fecha: '{fecha_limpia}'")
                
                # Intentar diferentes formatos
                formatos = ['%Y-%m-%d %H:%M', '%Y-%m-%d']
                fecha_valor = None
                
                for formato in formatos:
                    try:
                        fecha_valor = datetime.datetime.strptime(fecha_limpia, formato)
                        print(f"Usando fecha del BCV: {fecha_valor}")
                        return fecha_valor
                    except ValueError:
                        continue
                        
                if not fecha_valor:
                    print(f"Error parseando fecha {fecha_valor_str}, usando fecha actual")
                    return datetime.datetime.now()
                    
            except Exception as e:
                print(f"Error general parseando fecha: {e}")
                return datetime.datetime.now()
    else:
        return datetime.datetime.now()