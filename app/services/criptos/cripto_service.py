from datetime import datetime
from app.models.monitor import Monitor
from app.services.orchestrator import get_last_record, percent_change, set_color, set_symbol
from app.utils.date_utils import get_current_date_custom, parse_custom_date
from config.database import db
from config.logger import Logger

class CriptoService:

    currency = 'VES_XRP'
    title = 'XRP Ledger'
    currency_type = 2
    logger = Logger().get_logger("CriptoService")
        

    def get_cripto_by_id(self, cript_id):
        return self.cript_repository.find_by_id(cript_id)

    def get_all_criptos(self):
        return self.cript_repository.find_all()

    def create_cripto(self, price):
        try:
            db.connect(reuse_if_open=True)
            # Extraer fecha_valor del diccionario      
            last_record = get_last_record(self.currency, self.title)
            
            # Si no hay registros previos (last_update es None), crear nuevo registro
            if last_record.last_update is None:
                self.save_cripto(price, last_record.price, last_record.last_update, self.currency, self.title, self.currency_type)
                print(f"✅ Tasa de {self.title} guardada en la base de datos.")
            else:
                # Si hay registros, comparar por fecha
                if last_record.last_update.date() != datetime.now().date():
                    self.save_cripto(price, last_record.price, last_record.last_update, self.currency, self.title, self.currency_type)
                    print("✅ Tasa de Binance P2P guardada en la base de datos.")
                    self.logger.info(f"✅ Tasa guardada correctamente: {self.title}")
                elif last_record.last_update.date() == datetime.now().date():
                    self.update_cripto(price, last_record)
                    print("✅ Tasa de Binance P2P actualizada en la base de datos.")
                    self.logger.info(f"✅ Tasa actualizada correctamente: {self.title}")
        except Exception as e:
            print(f"❌ Error al guardar tasa de Binance P2P: {e}")
            self.logger.error(f"❌ Error al guardar tasa de Binance P2P: {e} create_cripto()")
            
        finally:
            if not db.is_closed():
                db.close()

    def save_cripto(self, price, price_db, last_update_date_db, currency, title, currency_type):
        try:
            Monitor.create(
                currency=currency,
                change=price - price_db if price_db else 0.0,
                color=set_color(price_db, price),
                image='https://www.svgrepo.com/show/331309/binance.svg',
                last_update=datetime.now(),
                last_update_old=last_update_date_db if last_update_date_db else parse_custom_date(get_current_date_custom()),
                percent=percent_change(price, price_db),
                price=float(price),
                currency_type=currency_type,
                price_old=price_db if price_db else 0.0,
                symbol=set_symbol(price_db, price),
                title=title
            )
            print(f"✅ Tasa guardada para VES_USDT: {price} con fecha {datetime.now()}")
            self.logger.info(f"✅ Tasa guardada para VES_USDT: {price} con fecha {datetime.now()}")
        except Exception as e:
            print(f"❌ Error al guardar tasa de Binance P2P: {e} save_cripto()")
            self.logger.error(f"❌ Error al guardar tasa de Binance P2P: {e} save_cripto()")
            return None

    def update_cripto(self, price, data_db: Monitor):

        try:
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
                (Monitor.currency == self.currency) & (Monitor.title == self.title)
            
            ).where(Monitor.id == data_db.id).execute()
            print(f"✅ Tasa actualizada para {self.title}: {price} con fecha {datetime.now()}")
            self.logger.info(f"✅ Tasa actualizada para {self.title}: {price} con fecha {datetime.now()}")   
        except Exception as e:
            print(f"❌ Error al actualizar la tasa {self.title}: {price} con fecha {datetime.datetime.now()} - {e}")
            self.logger.error((f"❌ Error al actualizar la tasa {self.title}: {price} con fecha {datetime.datetime.now()} - {e} update_cripto()"))

    def delete_cripto(self, cript_id):
        return self.cript_repository.delete(cript_id)