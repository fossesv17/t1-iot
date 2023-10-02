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

    def saveData(headers, dataInDict):

        config = Configuracion.select()[0]
        config_update = Configuracion.update()

        if(headers['ID_protocol']==0):
            toInsert = Datos(ID_device=headers['ID_device'], Device_MAC=headers['MAC'], Batt_level=dataInDict['Batt_level'])
            toInsert.save()

        elif(headers['ID_protocol']==1):
            toInsert = Datos(ID_device=headers['ID_device'], Device_MAC=headers['MAC'], Batt_level=dataInDict['Batt_level'], Timestamp=dataInDict['Timestamp'])
            toInsert.save()

        elif(headers['ID_protocol']==2):
            toInsert = Datos(ID_device=headers['ID_device'], Device_MAC=headers['MAC'], Batt_level=dataInDict['Batt_level'], Timestamp=dataInDict['Timestamp'], 
                             Temp=dataInDict['Temp'], Press=dataInDict['Press'], Hum=dataInDict['Hum'], Co=dataInDict['Co'])
            toInsert.save()

        elif(headers['ID_protocol']==3):
            toInsert = Datos(ID_device=headers['ID_device'], Device_MAC=headers['MAC'], Batt_level=dataInDict['Batt_level'], Timestamp=dataInDict['Timestamp'], 
                             Temp=dataInDict['Temp'], Press=dataInDict['Press'], Hum=dataInDict['Hum'], Co=dataInDict['Co'], RMS=dataInDict['RMS'], Amp_x=dataInDict['Amp_x'],
                             Frec_x=dataInDict['Frec_X'], Amp_y=dataInDict['Amp_Y'], Frec_y=dataInDict['Frec_Y'], Amp_z=dataInDict['Amp_Z'], Frec_z=dataInDict['Frec_Z'])
            toInsert.save()

        elif(headers['ID_protocol'] ==4):
            toInsert = Datos(ID_device=headers['ID_device'], Device_MAC=headers['MAC'], Batt_level=dataInDict['Batt_level'], Timestamp=dataInDict['Timestamp'], 
                             Temp=dataInDict['Temp'], Press=dataInDict['Press'], Hum=dataInDict['Hum'], Co=dataInDict['Co'], Acc_x=dataInDict['Acc_X'],
                             Acc_y=dataInDict['Acc_Y'], Acc_z=dataInDict['Acc_Z'], Rgyr_x=dataInDict['Rgyr_X'], Rgyr_y=dataInDict['Rgyr_Y'], Rgyr_z=dataInDict['Rgyr_Z'])
            toInsert.save()

        else:
            pass


class Datos(BaseModel):

    # Headers necesarios
    ID_device = CharField(max_length=2)
    Device_MAC = CharField(max_length=6)  
    
    # Datos Protocolo 0
    Batt_level = IntegerField()

    # Datos Protocolo 1
    Timestamp = DateTimeField()

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