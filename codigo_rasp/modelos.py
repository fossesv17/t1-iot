from peewee import Model, PostgresqlDatabase, ForeignKeyField, CharField, IntegerField, FloatField, DateTimeField, \
    BlobField

import psycopg2

# Configuración de la base de datos
hostname = 'localhost'
port_id = 5432
user = 'postgres'
password = 'postgres'
database = 'db'

db = PostgresqlDatabase('db',
                        host=hostname,
                        port=port_id,
                        user=user,
                        password=password)

conn = None
cur = None

try:

    conn = psycopg2.connect(host=hostname,
                            user=user,
                            password=password)

    cur = conn.cursor()

    create_datos_script = '''CREATE TABLE IF NOT EXISTS Datos(
                            IDdevice character(2) NOT NULL,
                            Device_MAC character(6) NOT NULL PRIMARY KEY,
                            Battlevel integer,
                            Timestamp timestamp(4),
                            Temp integer,
                            Press integer,
                            Hum integer,
                            Co real,
                            RMS real,
                            Ampx real,
                            Frecx real,
                            Ampy real,
                            Frecy real,
                            Ampz real,
                            Frecz real) '''

    create_config_script = '''CREATE TABLE IF NOT EXISTS Configuracion(
                            IDProtocol integer NOT NULL,
                            Transport_Layer character(1) NOT NULL)'''

    create_logs_script = '''CREATE TABLE IF NOT EXISTS Logs(
                            Timestmp timestamp(4) NOT NULL,
                            IDDevice character(2) NOT NULL,
                            IDProtocol integer NOT NULL,
                            Transport_Layer character(1) NOT NULL)'''

    create_loss_script = '''CREATE TABLE IF NOT EXISTS Loss(
                            TiempoDemora real NOT NULL,
                            PacketLoss int NOT NULL)'''

    cur.execute(create_datos_script)
    cur.execute(create_config_script)
    cur.execute(create_logs_script)
    cur.execute(create_loss_script)

    insert_to_datos_script = 'INSERT INTO Datos (IDDevice, Device_MAC, Battlevel, Timestamp, ' \
                             'Temp, Press, Hum, Co, RMS, Ampx, Frecx, Ampy, Frecy, Ampz, Frecz) VALUES ' \
                             '(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

    #insert_to_datos_values = ('Harry', '2C:41:A1:27:09:57', 80, '1999-01-08 04:05:06')

    conn.commit()

except Exception as error:
    print(error)
finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()


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

    class Meta:
        database = db
        db_table = 'Datos'


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


def update_config(id_protocol, trans_layer):
    # Tabla Configuracion
    config = Configuracion.select()
    if config is not None:
        for conf in config:
            if conf.ID_protocol != id_protocol or conf.Transport_Layer != trans_layer:
                conf.ID_protocol = id_protocol
                conf.Transport_Layer = trans_layer
                conf.save()
    else:
        new_config = Configuracion.create(ID_protocol=id_protocol, Transport_Layer=trans_layer)
        new_config.save()


def saveData(headers, dataInDict):
    # Verificamos la configuracion
    update_config(headers['ID_protocol'], headers['Transport_Layer'])

    # Tabla Datos
    if headers['ID_protocol'] == 0:
        toInsert = Datos.create(ID_device=headers['ID_device'], Device_MAC=headers['MAC'],
                                Batt_level=dataInDict['Batt_level'])

    elif headers['ID_protocol'] == 1:
        toInsert = Datos.create(ID_device=headers['ID_device'], Device_MAC=headers['MAC'],
                                Batt_level=dataInDict['Batt_level'], Timestamp=dataInDict['Timestamp'])

    elif headers['ID_protocol'] == 2:
        toInsert = Datos.create(ID_device=headers['ID_device'], Device_MAC=headers['MAC'],
                                Batt_level=dataInDict['Batt_level'], Timestamp=dataInDict['Timestamp'],
                                Temp=dataInDict['Temp'], Press=dataInDict['Press'], Hum=dataInDict['Hum'],
                                Co=dataInDict['Co'])

    elif headers['ID_protocol'] == 3:
        toInsert = Datos.create(ID_device=headers['ID_device'], Device_MAC=headers['MAC'],
                                Batt_level=dataInDict['Batt_level'], Timestamp=dataInDict['Timestamp'],
                                Temp=dataInDict['Temp'], Press=dataInDict['Press'], Hum=dataInDict['Hum'],
                                Co=dataInDict['Co'], RMS=dataInDict['RMS'], Amp_x=dataInDict['Amp_x'],
                                Frec_x=dataInDict['Frec_X'], Amp_y=dataInDict['Amp_Y'], Frec_y=dataInDict['Frec_Y'],
                                Amp_z=dataInDict['Amp_Z'], Frec_z=dataInDict['Frec_Z'])

    else:
        pass

# db.connect()
# db.create_tables([Datos, Configuracion, Logs, Loss])
