from peewee import Model, PostgresqlDatabase, CharField, IntegerField, FloatField, DateTimeField, BlobField

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
    ID_device = CharField(max_length=255)
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


class Logs(BaseModel):
    timestamp = DateTimeField()
    ID_device = CharField(max_length=255)

    # Headers necesarios
    Transport_Layer = CharField(max_length=1)
    ID_protocol = CharField(max_length=1)


class Configuracion(BaseModel):
    ID_device = CharField(max_length=255)

    # Headers necesarios
    Transport_Layer = CharField(max_length=1)
    ID_protocol = CharField(max_length=1)
    

class Loss(BaseModel):
    Tiempo_Demora = FloatField()
    Packet_Loss = IntegerField()


## Ver la documentación de peewee para más información, es super parecido a Django