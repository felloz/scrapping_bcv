from peewee import *
import datetime
from config.database import db

class Monitor(Model):
    currency = CharField()                  # Ej: 'bcv', 'enparalelovzla'
    change = FloatField()
    color = CharField()
    image = CharField()
    transaction_type = CharField()  # 1 para compra, 2 para venta
    last_update = DateTimeField()
    last_update_old = DateTimeField()          # Si luego decides usar DateTime, puedes cambiarlo
    percent = FloatField()
    price = FloatField()
    price_old = FloatField()
    symbol = CharField()
    currency_type = IntegerField()  # 1 para fiat, 2 para cripto
    title = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db
        table_name = 'monitors'
