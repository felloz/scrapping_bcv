from peewee import Model
from config.database import db

class BaseModel(Model):
    class Meta:
        database = db
