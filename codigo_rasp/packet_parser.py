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
    #print(packet[:37])
    values = dataToDict(protocol, packet[37:])
    return headers, values

def getDictHeader(packet):
    header = packet[:37]
    print(header)
    header = headerToDict(header)
    return header


def headerToDict(data):
    ID_Device, MAC, transport_layer, protocol, len_msg = unpack("<8s17s3i", data)
    dict = {"ID_device": ID_Device.decode().rstrip("\x00"), "MAC": MAC.decode().rstrip("\x00"), "ID_protocol": protocol,
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


def dataToDict(protocol, data):
    if protocol not in [0, 1, 2, 3]:
        print("Error: protocol doesnt exist")
        return None
    
    #print(data)
    data_dict = {}

    if protocol == 0:
        p0 = ["Batt_level"]

        batt_lvl = unpack("<H", data)

        data_dict[p0[0]] = batt_lvl

        return data_dict
    
    elif protocol == 1:
        p1 = ["Batt_level", "Timestamp"]
        
        batt_lvl, timestmp = unpack("<H19s", data)
        data1 = [batt_lvl, timestmp]

        for i in range(0, len(p1)):
            data_dict[p1[i]] = data1[i]

        return data_dict
    
    elif protocol == 2:
        p2 = ["Batt_level", "Timestamp", "Temp", "Press", "Hum", "Co"]

        batt_lvl, timestmp, temp, press, hum, co = unpack("<H19s4i", data)

        data2 = [batt_lvl, timestmp, temp, press, hum, co]

        for i in range(0, len(p2)):
            data_dict[p2[i]] = data2[i]

        return data_dict
    
    elif protocol == 3:
        p3 = ["Batt_level", "Timestamp", "Temp", "Press", "Hum", "Co", "RMS", "Amp_X", "Frec_X", "Amp_Y", "Frec_Y", "Amp_Z",
                "Frec_Z"]
        
        batt_lvl, timestmp, temp, press, hum, co, rms, ampx, frecx, ampy, frecy, ampz, frecz = unpack("<H19s4ifffffff", data)

        data3 = [batt_lvl, timestmp, temp, press, hum, co, rms, ampx, frecx, ampy, frecy, ampz, frecz]

        for i in range(0, len(p3)):
            data_dict[p3[i]] = data3[i]

        return data_dict

    else:
        print("Error")
            



# Probando si funciona el acceso a la base de datos desde otro archivo:

headers_datos_0 = {"ID_device": 'Barry', "MAC": '2C:41:A1:27:09:57', "ID_protocol": 1,
                        "Transport_layer": '1', "length": 51}

insert_to_datos_values = {"Batt_level": 75, "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Temp": 15, "Press": 1100,
                            "Hum": 55, "Co": 176, "RMS": 0.009, "Amp_X": 0.1, "Frec_X": 30.3, "Amp_Y": 0.05,
                            "Frec_Y": 59.1, "Amp_Z": 0.009, "Frec_Z": 90.2}

packed = packing(headers_datos_0, insert_to_datos_values)

#print(packed)

headers, values = unpacking(packed)

print(headers)
print(values)

#insert_to_Datos(headers_datos_0, insert_to_datos_values)
#insert_to_Logs(headers_datos_0, insert_to_datos_values)
#insert_to_Configuracion(headers_datos_0)
#config = get_current_config()
