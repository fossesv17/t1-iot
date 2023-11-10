import datetime

from peewee import Model, PostgresqlDatabase, ForeignKeyField, CharField, IntegerField, FloatField, DateTimeField, \
    BlobField

import psycopg2
import psycopg2.extras

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


def insert_to_Datos(headers, dataInDict):
    """
    :param headers: Un diccionario con los headers
    :param dataInDict: Un diccionario con todos los datos que se desean agregar
    """
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:

        id_protocol = headers['ID_protocol']

        if id_protocol == 0:
            insert_to_datos_script = 'INSERT INTO Datos (IDDevice, Device_MAC, Battlevel) VALUES ' \
                                     '(%s, %s, %s)'

            insert_to_datos_values = (headers['ID_device'], headers['MAC'], dataInDict['Batt_level'])

            cur.execute(insert_to_datos_script, insert_to_datos_values)

        elif id_protocol == 1:
            insert_to_datos_script = 'INSERT INTO Datos (IDDevice, Device_MAC, Battlevel, Timestamp) VALUES ' \
                                     '(%s, %s, %s, %s)'

            insert_to_datos_values = (headers['ID_device'], headers['MAC'], dataInDict['Batt_level'],
                                      dataInDict['Timestamp'])

            cur.execute(insert_to_datos_script, insert_to_datos_values)

        elif id_protocol == 2:
            insert_to_datos_script = 'INSERT INTO Datos (IDDevice, Device_MAC, Battlevel, Timestamp, ' \
                                     'Temp, Press, Hum, Co) VALUES ' \
                                     '(%s, %s, %s, %s, %s, %s, %s, %s)'

            insert_to_datos_values = (headers['ID_device'], headers['MAC'], dataInDict['Batt_level'],
                                      dataInDict['Timestamp'], dataInDict['Temp'], dataInDict['Press'],
                                      dataInDict['Hum'], dataInDict['Co'])

            cur.execute(insert_to_datos_script, insert_to_datos_values)
        else:
            insert_to_datos_script = 'INSERT INTO Datos (IDDevice, Device_MAC, Battlevel, Timestamp, ' \
                                     'Temp, Press, Hum, Co, RMS, Ampx, Frecx, Ampy, Frecy, Ampz, Frecz) VALUES ' \
                                     '(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

            insert_to_datos_values = (headers['ID_device'], headers['MAC'], dataInDict['Batt_level'],
                                      dataInDict['Timestamp'], dataInDict['Temp'], dataInDict['Press'],
                                      dataInDict['Hum'], dataInDict['Co'], dataInDict['RMS'], dataInDict['Amp_X'],
                                      dataInDict['Frec_X'], dataInDict['Amp_Y'], dataInDict['Frec_Y'],
                                      dataInDict['Amp_Z'], dataInDict['Frec_Z'])

            cur.execute(insert_to_datos_script, insert_to_datos_values)


def insert_to_Configuracion(headers):
    """
    :param headers: Un diccionario con los headers
    """
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        protocol = headers['ID_protocol']
        trans_layer = headers['Transport_layer']

        insert_script = 'INSERT INTO Configuracion (IDProtocol, TransportLayer) VALUES (%s, %s)'
        insert_values = (protocol, trans_layer)
        cur.execute(insert_script, insert_values)


def insert_to_Logs(headers, dataInDict):
    """
    :param headers: Un diccionario con los headers
    :param dataInDict: Un diccionario con todos los datos que se desean agregar
    """
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        insert_to_logs_script = 'INSERT INTO Logs (Timestamp, IDDevice, IDProtocol, TransportLayer) VALUES ' \
                                '(%s, %s, %s, %s)'

        insert_to_logs_values = (dataInDict['Timestamp'], headers['ID_device'], headers['ID_protocol'],
                                 headers['Transport_layer'])

        cur.execute(insert_to_logs_script, insert_to_logs_values)


def insert_to_Loss(headers, dataInDict):
    """
    :param headers: Un diccionario con los headers
    :param dataInDict: Un diccionario con todos los datos que se desean agregar
    """
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        expected_len = headers['length']

        real_len = len(dataInDict.values())

        diff = expected_len - real_len

        insert_to_loss_script = 'INSERT INTO Loss (TiempoDemora, PacketLoss) VALUES (%s, %s)'

        fecha1 = dataInDict['Timestamp']
        fecha2 = datetime.datetime.now()

        fecha1_hours = int(datetime.datetime.strptime(fecha1, '%Y-%m-%d %H:%M:%S').strftime('%H'))
        fecha1_minutes = int(datetime.datetime.strptime(fecha1, '%Y-%m-%d %H:%M:%S').strftime('%M'))
        fecha1_seconds = int(datetime.datetime.strptime(fecha1, '%Y-%m-%d %H:%M:%S').strftime('%S'))

        fecha2_hours = int(fecha2.strftime('%H'))
        fecha2_minutes = int(fecha2.strftime('%M'))
        fecha2_seconds = int(fecha2.strftime('%S'))

        seconds = 3600 * (fecha2_hours - fecha1_hours) + 60 * (fecha2_minutes - fecha1_minutes) + \
                  (fecha2_seconds - fecha1_seconds)

        insert_to_loss_values = (seconds, diff)

        cur.execute(insert_to_loss_script, insert_to_loss_values)


cur = None

try:

    with psycopg2.connect(host=hostname,
                          user=user,
                          password=password) as conn:

        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            # Baja las tablas en caso de existir previamente
            cur.execute('DROP TABLE IF EXISTS Datos')
            cur.execute('DROP TABLE IF EXISTS Configuracion')
            cur.execute('DROP TABLE IF EXISTS Logs')
            cur.execute('DROP TABLE IF EXISTS Loss')

            # Scripts para crear las tablas
            create_datos_script = '''CREATE TABLE IF NOT EXISTS Datos(
                                    IDdevice character(8) NOT NULL,
                                    Device_MAC character(18) NOT NULL,
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
                                    TransportLayer character(3) NOT NULL)'''

            create_logs_script = '''CREATE TABLE IF NOT EXISTS Logs(
                                    Timestamp timestamp(4) NOT NULL,
                                    IDDevice character(8) NOT NULL,
                                    IDProtocol integer NOT NULL,
                                    TransportLayer character(3) NOT NULL)'''

            create_loss_script = '''CREATE TABLE IF NOT EXISTS Loss(
                                    TiempoDemora real NOT NULL,
                                    PacketLoss int NOT NULL)'''

            cur.execute(create_datos_script)
            cur.execute(create_config_script)
            cur.execute(create_logs_script)
            cur.execute(create_loss_script)

            # Ejemplos donde se agregan datos manualmente

            headers_datos_0 = {"ID_device": 'Harry', "MAC": '2C:41:A1:27:09:57', "ID_protocol": 0,
                               "Transport_layer": 'TCP', "length": 27}

            headers_datos_1 = {"ID_device": 'Henry', "MAC": '2C:41:A1:27:09:57', "ID_protocol": 1,
                               "Transport_layer": 'TCP', "length": 31}

            headers_datos_2 = {"ID_device": 'Larry', "MAC": '2C:41:A1:27:09:57', "ID_protocol": 2,
                               "Transport_layer": 'TCP', "length": 41}

            headers_datos_3 = {"ID_device": 'Jerry', "MAC": '2C:41:A1:27:09:57', "ID_protocol": 3,
                               "Transport_layer": 'TCP', "length": 69}

            headers = (headers_datos_0, headers_datos_1, headers_datos_2, headers_datos_3)

            insert_to_datos_values = {"Batt_level": 80, "Timestamp": '2023-10-08 04:05:06', "Temp": 15, "Press": 1100,
                                      "Hum": 55, "Co": 176, "RMS": 0.009, "Amp_X": 0.1, "Frec_X": 30.3, "Amp_Y": 0.05,
                                      "Frec_Y": 59.1, "Amp_Z": 0.009, "Frec_Z": 90.2}

            for header in headers:
                insert_to_Datos(header, insert_to_datos_values)
                insert_to_Logs(header, insert_to_datos_values)
                insert_to_Loss(header, insert_to_datos_values)
                insert_to_Configuracion(header)


except Exception as error:
    print(error)
finally:
    if conn is not None:
        conn.close()


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
