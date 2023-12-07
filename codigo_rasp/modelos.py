import datetime

from peewee import Model, PostgresqlDatabase, ForeignKeyField, CharField, IntegerField, FloatField, DateTimeField, \
    BlobField

import psycopg2
import psycopg2.extras

'''
- Correr el archivo "modelos.py", esto creará las tablas de la base de datos.
- Para insertar datos, se puede usar la función específica para cada tabla. Por ejemplo, si queremos agregar datos a la tabla "Loss", 
debemos invocar la función "insert_to_Loss(...)", con los parámetros correspondientes. Salvo para configuración, las funciones reciben 
dos parámetros: los headers y los datos que se desean agregar. Ambos parámetros son diccionarios. 
- La función de configuración solo recibe el parámetros de los headers pues no utiliza ni almacena información relacionada a los datos.
- La función "unpacking", del archivo packet_parser.py deberia retornar ambos diccionarios listos, de modo que se pueda utilizar
una logica de insercion como la siguiente:
    -> headers, data = unpacking(a_pack)
    -> insert_to_Datos(headers, data)
'''

# Configuración de la base de datos
hostname = 'db'
port_id = 5432
user = 'postgres'
password = 'postgres'
database = 'iot_db'

db = PostgresqlDatabase('iot_db',
                        host=hostname,
                        port=port_id,
                        user=user,
                        password=password)

cur = None

def insert_to_Datos(headers, dataInDict):
    """
    :param headers: Un diccionario con los headers
    :param dataInDict: Un diccionario con todos los datos que se desean agregar
    """

    try:

        with psycopg2.connect(host=hostname,
                            user=user,
                            password=password) as conn:
            
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
                elif id_protocol == 3:
                    insert_to_datos_script = 'INSERT INTO Datos (IDDevice, Device_MAC, Battlevel, Timestamp, ' \
                                            'Temp, Press, Hum, Co, RMS, Ampx, Frecx, Ampy, Frecy, Ampz, Frecz) VALUES ' \
                                            '(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

                    insert_to_datos_values = (headers['ID_device'], headers['MAC'], dataInDict['Batt_level'],
                                            dataInDict['Timestamp'], dataInDict['Temp'], dataInDict['Press'],
                                            dataInDict['Hum'], dataInDict['Co'], dataInDict['RMS'], dataInDict['Amp_X'],
                                            dataInDict['Frec_X'], dataInDict['Amp_Y'], dataInDict['Frec_Y'],
                                            dataInDict['Amp_Z'], dataInDict['Frec_Z'])

                    cur.execute(insert_to_datos_script, insert_to_datos_values)
                else:
                    insert_to_datos_script = 'INSERT INTO Datos (IDDevice, Device_MAC, Battlevel, Timestamp, ' \
                                            'Temp, Press, Hum, Co, Accx, Accy, Accz, Rgyrx, Rgyry, Rgyrz) VALUES ' \
                                            '(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                    
                    insert_to_datos_values = (headers['ID_device'], headers['MAC'], dataInDict['Batt_level'],
                                            dataInDict['Timestamp'], dataInDict['Temp'], dataInDict['Press'],
                                            dataInDict['Hum'], dataInDict['Co'], dataInDict['Acc_X'], dataInDict['Acc_Y'],
                                            dataInDict['Acc_Z'], dataInDict['Rgyr_X'], dataInDict['Rgyr_Y'],
                                            dataInDict['Rgyr_Z'])                    

                    cur.execute(insert_to_datos_script, insert_to_datos_values)
                    
    except Exception as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def insert_to_Configuracion(headers, dataInDict):
    """
    :param headers: Un diccionario con los headers
    :param dataInDict: Un diccionario con todos los datos que deben introducirse en esta tabla
    """
    try:

        with psycopg2.connect(host=hostname,
                            user=user,
                            password=password) as conn:
            
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                protocol = headers['ID_protocol']
                trans_layer = headers['Transport_layer']

                TCP_port = dataInDict['TCP_Port']
                UDP_port = dataInDict['UDP_Port']
                Gyro_sensibility = dataInDict['Gyro_Sensibility']
                Acc_sensibility = dataInDict['Acc_Sensibility']
                Acc_srate = dataInDict['Acc_SRate']
                Gyro_srate = dataInDict['Gyro_SRate']
                Disc_time = dataInDict['Disc_Time']
                Host_ip_addr = dataInDict['Host_IP_Address']
                Wifi_ssid = dataInDict['Wifi_SSID']
                Wifi_pass = dataInDict['Wifi_Pass']


                insert_script = '''INSERT INTO Configuracion (Timestamp, IDProtocol, TransportLayer, TCP_Port, UDP_Port, GyroSensibility,
                AccSensibility, GyroSamplingRate, AccSamplingRate, DiscTime, HostIpAddr, WifiSSID, WifiPass) VALUES (%s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s)'''
                insert_values = (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), protocol, trans_layer, TCP_port, UDP_port, Gyro_sensibility, Acc_sensibility,
                                 Gyro_srate, Acc_srate, Disc_time, Host_ip_addr, Wifi_ssid, Wifi_pass)

                cur.execute(insert_script, insert_values)

    except Exception as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def insert_to_Logs(headers, dataInDict):
    """
    :param headers: Un diccionario con los headers
    :param dataInDict: Un diccionario con todos los datos que se desean agregar
    """
    try:
        with psycopg2.connect(host=hostname,
                            user=user,
                            password=password) as conn:
            
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                insert_to_logs_script = 'INSERT INTO Logs (Timestamp, IDDevice, IDProtocol, TransportLayer) VALUES ' \
                                        '(%s, %s, %s, %s)'

                insert_to_logs_values = (dataInDict['Timestamp'], headers['ID_device'], headers['ID_protocol'],
                                        headers['Transport_layer'])

                cur.execute(insert_to_logs_script, insert_to_logs_values)

    except Exception as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def insert_to_Loss(headers, dataInDict):
    """
    :param headers: Un diccionario con los headers
    :param dataInDict: Un diccionario con todos los datos que se desean agregar
    """
    try:
        with psycopg2.connect(host=hostname,
                            user=user,
                            password=password) as conn:
            
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                expected_len = headers['length'] - 12

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

    except Exception as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def get_current_config():
    """
    :return: Retorna la configuracion mas reciente
    """
    try:
        with psycopg2.connect(host=hostname,
                            user=user,
                            password=password) as conn:
            
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.execute('SELECT * FROM Configuracion ORDER BY TIMESTAMP DESC')
                config = cur.fetchone()

                protocol = config[1]
                transport_layer = config[2]
                tcp_port = config[3]
                udp_port = config[4]
                gyro_sens = config[5]
                acc_sens = config[6]
                gyro_srate = config[7]
                acc_srate = config[8]
                disc_time = config[9]
                host_ip_addr = config[10]
                wifi_ssid = config[11]
                wifi_pass = config[12]


                return protocol, transport_layer, tcp_port, udp_port, gyro_sens, acc_sens, gyro_srate, acc_srate, \
                        disc_time, host_ip_addr, wifi_ssid, wifi_pass
    finally:
        if conn is not None:
            conn.close()

def create_tables():
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
                                        Frecz real,
                                        Accx text[],
                                        Accy text[],
                                        Accz text[],
                                        Rgyrx text[],
                                        Rgyry text[],
                                        Rgyrz text[]) '''

                create_config_script = '''CREATE TABLE IF NOT EXISTS Configuracion(
                                        Timestamp timestamp(4) NOT NULL,
                                        IDProtocol integer NOT NULL,
                                        TransportLayer character(1) NOT NULL,
                                        TCP_Port integer ,
                                        UDP_Port integer,
                                        GyroSensibility integer,
                                        AccSensibility integer,
                                        GyroSamplingRate integer,
                                        AccSamplingRate integer ,
                                        DiscTime integer,
                                        HostIpAddr varchar(32),
                                        WifiSSID varchar,
                                        WifiPass varchar)'''

                create_logs_script = '''CREATE TABLE IF NOT EXISTS Logs(
                                        Timestamp timestamp(4) NOT NULL,
                                        IDDevice character(8) NOT NULL,
                                        IDProtocol integer NOT NULL,
                                        TransportLayer character(1) NOT NULL)'''

                create_loss_script = '''CREATE TABLE IF NOT EXISTS Loss(
                                        TiempoDemora real NOT NULL,
                                        PacketLoss int NOT NULL)'''

                cur.execute(create_datos_script)
                cur.execute(create_config_script)
                cur.execute(create_logs_script)
                cur.execute(create_loss_script)

            conn.close()

    except Exception as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

# if __name__ == "__main__":
#     create_tables()
#     headers_datos = {"ID_device": 'Barry', "MAC": '2C:41:A1:27:09:57', "Transport_layer": '1', "ID_protocol": 2, "length": 51}
#     insert_to_datos_values = {"Batt_level": 75, "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Temp": 15, "Press": 1100, 
#                             "Hum": 55, "Co": 176, "RMS": 0.009, "Amp_X": 0.1, "Frec_X": 30.3, "Amp_Y": 0.05,
#                             "Frec_Y": 59.1, "Amp_Z": 0.009, "Frec_Z": 90.2}
#     insert_to_Datos(headers_datos, insert_to_datos_values)


