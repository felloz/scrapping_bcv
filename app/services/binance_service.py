from config.database import db
from datetime import datetime
from app.models.monitor import Monitor
from app.services.orchestrator import get_last_record, percent_change, set_color, set_symbol
from app.utils.date_utils import get_current_date_custom, parse_custom_date


def save_binance_rate(price):
    try:
        db.connect(reuse_if_open=True)
        # Extraer fecha_valor del diccionario      
        last_record = get_last_record('VES_USDT', 'Binance P2P')
        
        # Si no hay registros previos (last_update es None), crear nuevo registro
        if last_record.last_update is None:
            store_binance_data(price, last_record.price, last_record.last_update)
            print("✅ Tasa de Binance P2P guardada en la base de datos.")
        else:
            # Si hay registros, comparar por fecha
            if last_record.last_update.date() != datetime.now().date():
                store_binance_data(price, last_record.price, last_record.last_update)
                print("✅ Tasa de Binance P2P guardada en la base de datos.")
            elif last_record.last_update.date() == datetime.now().date():
                update_binance_rate(price, last_record)
                print("✅ Tasa de Binance P2P actualizada en la base de datos.")
    except Exception as e:
        print(f"❌ Error al guardar tasa de Binance P2P: {e}")
    finally:
        if not db.is_closed():
            db.close()


def store_binance_data(price, price_db, last_update_date_db):
    try:
        Monitor.create(
            currency='VES_USDT',
            change=price - price_db if price_db else 0.0,
            color=set_color(price_db, price),
            image='https://www.svgrepo.com/show/331309/binance.svg',
            last_update=datetime.now(),
            last_update_old=last_update_date_db if last_update_date_db else parse_custom_date(get_current_date_custom()),
            percent=percent_change(price, price_db),
            price=float(price),
            price_old=price_db if price_db else 0.0,
            symbol=set_symbol(price_db, price),
            title='Binance P2P'
        )
        print(f"✅ Tasa guardada para VES_USDT: {price} con fecha {datetime.now()}")
    except Exception as e:
        print(f"❌ Error al guardar tasa de Binance P2P: {e}")
        return None 


def update_binance_rate(price, data_db: Monitor):
    Monitor.update(
        change=price - data_db.price if data_db.price else 0.0,
        color=set_color(data_db.price, price),
        last_update=datetime.now(),
        last_update_old=data_db.last_update if data_db.last_update else parse_custom_date(get_current_date_custom()),
        percent=percent_change(price, data_db.price),
        price=float(price),
        price_old=data_db.price if data_db.price else 0.0,
        symbol=set_symbol(data_db.price, price),
    ).where(
        (Monitor.currency == 'VES_USDT') & (Monitor.title == 'Binance P2P')
    
    ).where(Monitor.id == data_db.id).execute()
    print(f"✅ Tasa actualizada para VES_USDT: {price} con fecha {datetime.now()}")       