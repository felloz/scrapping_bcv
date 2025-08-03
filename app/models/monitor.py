from peewee import *
import datetime
from config.database import db

class Monitor(Model):
    currency = CharField()                  # Ej: 'bcv', 'enparalelovzla'
    change = FloatField()
    color = CharField()
    image = CharField()
    last_update = DateTimeField()
    last_update_old = DateTimeField()          # Si luego decides usar DateTime, puedes cambiarlo
    percent = FloatField()
    price = FloatField()
    price_old = FloatField()
    symbol = CharField()
    title = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db
        table_name = 'monitors'
