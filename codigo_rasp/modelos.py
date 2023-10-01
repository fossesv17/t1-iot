from peewee import Model, PostgresqlDatabase, ForeignKeyField, CharField, IntegerField, FloatField, DateTimeField, BlobField

# Configuración de la base de datos
db_config = {
    'host': 'localhost', 
    'port': 5432, 
    'user': 'postgres', 
    'password': 'postgres', 
    'database': 'db'
}
db = PostgresqlDatabase(**db_config)

# Definición de un modelo
class BaseModel(Model):
    class Meta:
        database = db


class Datos(BaseModel):

    # Headers necesarios
    ID_device = CharField(max_length=2)
    Device_MAC = CharField(max_length=6)  
    
    # Datos Protocolo 0
    Batt_level = IntegerField()

    # Datos Protocolo 1
    timestamp = DateTimeField()

    # Datos Protocolo 2
    Temp = IntegerField()
    Press = IntegerField()
    Hum = IntegerField()
    Co = FloatField()

    # Datos Protocolo 3
    RMS = FloatField()
    Amp_x = FloatField()
    Frec_x = FloatField()
    Amp_y = FloatField()
    Frec_y = FloatField()
    Amp_z = FloatField()
    Frec_z = FloatField()

    # Datos Protocolo 4
    Acc_x = BlobField()
    Acc_y = BlobField()
    Acc_z = BlobField()
    Rgyr_x = BlobField()
    Rgyr_y = BlobField()
    Rgyr_z = BlobField()


class Configuracion(BaseModel):
    ID_device = ForeignKeyField(Datos)

    # Headers necesarios
    ID_protocol = CharField(max_length=1)
    Transport_Layer = CharField(max_length=1)
    


class Logs(BaseModel):
    timestamp = ForeignKeyField(Datos)
    ID_device = ForeignKeyField(Datos)

    # Headers necesarios
    ID_protocol = ForeignKeyField(Configuracion)
    Transport_Layer = ForeignKeyField(Configuracion)
    

class Loss(BaseModel):
    Tiempo_Demora = FloatField()
    Packet_Loss = IntegerField()


db.connect()
db.create_tables([Datos, Configuracion, Logs, Loss])

## Ver la documentación de peewee para más información, es super parecido a Django