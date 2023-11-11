from struct import unpack, pack
from pickle import dumps, loads
import datetime
import traceback
from modelos import *

# Documentación struct unpack,pack :https://docs.python.org/3/library/struct.html#

'''
-getDictHeader: Recibe el paquete en bytes, extrae los headers y retorna un diccionario con la informacion
-headerToDict: Transforma los headers en un diccionario con la informacion correspondiente.
-dictToHeader: Recibe un diccionario con los headers y los empaqueta
-dictToData: Se encarga de empaquetar la informacion a partir de un diccionario con la data
-protocolUnpack: desempaqueta los datos del mensaje
-dataToDict: Se encarga de desempaquetar. Transforma el area de datos en un diccionario con los datos del mensaje
-parseData: Utiliza dataToDict para obtener los datos y luego los almacena en la base de datos
'''


def packing(headers, data):
    packed_headers = dictToHeader(headers)
    packed_data = dictToData(headers, data)
    return packed_headers+packed_data


def unpacking(packet):
    headers = getDictHeader(packet)
    protocol = headers['ID_protocol']
    values = dataToDict(protocol, packet[37:])
    return headers, values

def getDictHeader(packet):
    header = packet[:37]
    header = headerToDict(header)
    return header


def headerToDict(data):
    ID_Device, MAC, transport_layer, protocol, len_msg = unpack("<8s17s3i", data)
    dict = {"ID_device": ID_Device.decode(), "MAC": MAC.decode(), "ID_protocol": protocol,
            "Transport_layer": transport_layer,
            "length": len_msg}
    return dict


def dictToHeader(dict):
    id_device = dict['ID_device']
    mac = dict['MAC']
    protocol = int(dict['ID_protocol'])
    trans_layer = int(dict['Transport_layer'])
    length = int(dict['length'])

    paquete = pack("<8s17s3i", id_device.encode(), mac.encode(), protocol, trans_layer, length)
    return paquete


def dictToData(headers, dict):
    id_protocol = headers['ID_protocol']

    if id_protocol == 0:
        batt_lvl = dict['Batt_level']
        return pack("<H", batt_lvl)

    elif id_protocol == 1:
        batt_lvl = dict['Batt_level']
        timestp = str(dict['Timestamp']).encode()

        return pack("<H19s", batt_lvl, timestp)

    elif id_protocol == 2:
        batt_lvl = dict['Batt_level']
        timestp = str(dict['Timestamp']).encode()

        temp = dict['Temp']
        press = dict['Press']
        hum = dict['Hum']
        co = dict['Co']

        return pack("<H19s4i", batt_lvl, timestp, temp, press, hum, co)
    else:
        batt_lvl = dict['Batt_level']
        timestp = str(dict['Timestamp']).encode()

        temp = dict['Temp']
        press = dict['Press']
        hum = dict['Hum']
        co = dict['Co']

        rms = dict['RMS']
        ampx = dict['Amp_X']
        frecx = dict['Frec_X']
        ampy = dict['Amp_Y']
        frecy = dict['Frec_Y']
        ampz = dict['Amp_Z']
        frecz = dict['Frec_Z']

        return pack("<H19s4ifffffff", batt_lvl, timestp, temp, press, hum, co,
                    rms, ampx, frecx, ampy, frecy, ampz, frecz)


def parseData(header, packet):
    dictData = dataToDict(header["ID_protocol"], packet)
    if dictData is not None:
        insert_to_Datos(header, dictData)
    return None if dictData is None else {**header, **dictData}


def protocolUnpack(protocol: int, data):
    print("Hola".encode() + data)
    protocol_unpack = ["<H", "<H19s", "<H19s4i", "<H19s4i7f"]
    return unpack(protocol_unpack[protocol], data)


def dataToDict(protocol: int, data):
    if protocol not in [0, 1, 2, 3]:
        print("Error: protocol doesnt exist")
        return None

    def protocolFunc(protocol, keys):
        def p(data):
            unp = protocolUnpack(protocol, data)
            data_dict = {}
            for (key, val) in zip(keys, unp):
                if key == "Timestamp":
                    data_dict[key] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(data_dict[key])
                else:
                    data_dict[key] = val
            return data_dict
        return p

    p0 = ["Batt_level"]
    p1 = ["Batt_level", "Timestamp"]
    p2 = ["Batt_level", "Timestamp", "Temp", "Press", "Hum", "Co"]
    p3 = ["Batt_level", "Timestamp", "Temp", "Press", "Hum", "Co", "RMS", "Amp_X", "Frec_X", "Amp_Y", "Frec_Y", "Amp_Z",
          "Frec_Z"]

    p = [p0, p1, p2, p3]

    try:
        return protocolFunc(protocol, p[protocol])(data)
    except Exception:
        print("Data unpacking Error:", traceback.format_exc())
        return None


headers_datos_0 = {"ID_device": 'Harry', "MAC": '2C:41:A1:27:09:57', "ID_protocol": 0,
                   "Transport_layer": 1, "length": 70}

datos_values = {"Batt_level": 80, "Timestamp": '2023-10-08 04:05:06', "Temp": 15, "Press": 1100,
                          "Hum": 55, "Co": 176, "RMS": 0.009, "Amp_X": 0.1, "Frec_X": 30.3, "Amp_Y": 0.05,
                          "Frec_Y": 59.1, "Amp_Z": 0.009, "Frec_Z": 90.2}


