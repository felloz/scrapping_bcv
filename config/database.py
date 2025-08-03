from peewee import PostgresqlDatabase

db = PostgresqlDatabase(
    'cambio_express',
    user='felloz',
    password='1234',
    host='192.168.180.128',
    port=5432
)
