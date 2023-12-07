from struct import unpack, pack, calcsize
from pickle import dumps, loads
import numpy
import datetime
import traceback
from modelos import *

# Documentación struct unpack,pack :https://docs.python.org/3/library/struct.html#

'''
-packing: Función compuesta que se encarga de empaquetar los diccionarios headers y data
-unpacking: Función compuesta que se encarga de desempaquetar, retorna dos diccionarios: los headers y la data
-getDictHeader: Recibe el paquete en bytes, extrae los headers y retorna un diccionario con la informacion
-headerToDict: Transforma los headers en un diccionario con la informacion correspondiente.
-dictToHeader: Recibe un diccionario con los headers y los empaqueta
-dictToData: Se encarga de empaquetar la informacion a partir de un diccionario con la data
-dataToDict: Se encarga de desempaquetar. Transforma el area de datos en un diccionario con los datos del mensaje
'''

DATA_FORMAT = ["<B", "<BL", "<BLBLBf", "<BLBLBfLLLLLLL", "<BLBLBf2000f2000f2000f2000f2000f2000f"]
HEADER_FORMAT = "<H6BBBH"

# def packing(headers, data):
#     packed_headers = dictToHeader(headers)
#     packed_data = dictToData(headers, data)
#     return packed_headers+packed_data


def unpacking(packet):
    headers = getDictHeader(packet)
    protocol = headers['ID_protocol']   
    # print(protocol)
    values = dataToDict(protocol, packet[12:])
    return headers, values

def getDictHeader(packet):
    header = packet[:12]
    header = headerToDict(header)
    # print(header)
    return header


def headerToDict(data):
    ID_Device, M1, M2, M3, M4, M5, M6, transport_layer, protocol, len_msg = unpack(HEADER_FORMAT, data)
    MAC = ".".join([hex(x)[2:] for x in [M1, M2, M3, M4, M5, M6]])
    dict = {"ID_device": ID_Device, "MAC": MAC, "Transport_layer": transport_layer,
             "ID_protocol": protocol, "length": len_msg}
    return dict


# def dictToHeader(dict):
#     id_device = dict['ID_device']
#     mac = dict['MAC']
#     protocol = int(dict['ID_protocol'])
#     trans_layer = int(dict['Transport_layer'])
#     length = int(dict['length'])

#     paquete = pack("H16sBBH", id_device.encode(), mac.encode(), trans_layer, protocol, length)
#     return paquete


# def dictToData(headers, dict):
#     id_protocol = headers['ID_protocol']

#     if id_protocol == 0:
#         batt_lvl = dict['Batt_level']
#         return pack(DATA_FORMAT[id_protocol], batt_lvl)

#     elif id_protocol == 1:
#         batt_lvl = dict['Batt_level']
#         timestp = str(dict['Timestamp']).encode()

#         return pack(DATA_FORMAT[id_protocol], batt_lvl, timestp)

#     elif id_protocol == 2:
#         batt_lvl = dict['Batt_level']
#         timestp = str(dict['Timestamp']).encode()

#         temp = dict['Temp']
#         press = dict['Press']
#         hum = dict['Hum']
#         co = dict['Co']

#         return pack(DATA_FORMAT[id_protocol], batt_lvl, timestp, temp, press, hum, co)
#     elif id_protocol == 3:
#         batt_lvl = dict['Batt_level']
#         timestp = str(dict['Timestamp']).encode()

#         temp = dict['Temp']
#         press = dict['Press']
#         hum = dict['Hum']
#         co = dict['Co']

#         rms = dict['RMS']
#         ampx = dict['Amp_X']
#         frecx = dict['Frec_X']
#         ampy = dict['Amp_Y']
#         frecy = dict['Frec_Y']
#         ampz = dict['Amp_Z']
#         frecz = dict['Frec_Z']

#         return pack(DATA_FORMAT[id_protocol], batt_lvl, timestp, temp, press, hum, co,
#                     rms, ampx, frecx, ampy, frecy, ampz, frecz)
#     elif id_protocol == 4:
#         batt_lvl = dict['Batt_level']
#         timestp = str(dict['Timestamp']).encode()

#         temp = dict['Temp']
#         press = dict['Press']
#         hum = dict['Hum']
#         co = dict['Co']

#         accx = dict['Acc_X']
#         accy = dict['Acc_Y']
#         accz = dict['Acc_Z']
#         rgyrx = dict['Rgyr_X']
#         rgyry = dict['Rgyr_Y']
#         rgyrz = dict['Rgyr_Z']

#         accx_packed = pack("<{}f".format(2000), *accx)
#         accy_packed = pack("<{}f".format(2000), *accy)
#         accz_packed = pack("<{}f".format(2000), *accz)
#         rgyrx_packed = pack("<{}f".format(2000), *rgyrx)
#         rgyry_packed = pack("<{}f".format(2000), *rgyry)
#         rgyrz_packed = pack("<{}f".format(2000), *rgyrz)

#         rest_pack = pack("<BLBLBf", batt_lvl, timestp, temp, press, hum, co)
#         return rest_pack+accx_packed+accy_packed+accz_packed+rgyrx_packed+rgyry_packed+rgyrz_packed
#     else:
#         print("Error")

def dataToDict(protocol, data):
    if protocol not in [0, 1, 2, 3, 4]:
        print("Error: protocol doesnt exist")
        return None
    
    #print(data)
    data_dict = {}

    if protocol == 0:
        p0 = ["Batt_level"]

        batt_lvl = unpack(DATA_FORMAT[protocol], data)[0]

        data_dict[p0[0]] = batt_lvl

        return data_dict
    
    elif protocol == 1:
        p1 = ["Batt_level", "Timestamp"]
        
        batt_lvl, timestmp = unpack(DATA_FORMAT[protocol], data)
        data1 = [batt_lvl, timestmp]

        for i in range(0, len(p1)):
            data_dict[p1[i]] = data1[i]

        return data_dict
    
    elif protocol == 2:
        p2 = ["Batt_level", "Timestamp", "Temp", "Press", "Hum", "Co"]

        batt_lvl, timestmp, temp, press, hum, co = unpack(DATA_FORMAT[protocol], data)

        data2 = [batt_lvl, timestmp, temp, press, hum, co]

        for i in range(0, len(p2)):
            data_dict[p2[i]] = data2[i]

        return data_dict
    
    elif protocol == 3:
        p3 = ["Batt_level", "Timestamp", "Temp", "Press", "Hum", "Co", "RMS", "Amp_X", "Frec_X", "Amp_Y", "Frec_Y", "Amp_Z",
                "Frec_Z"]
        
        batt_lvl, timestmp, temp, press, hum, co, rms, ampx, frecx, ampy, frecy, ampz, frecz = unpack(DATA_FORMAT[protocol], data)

        data3 = [batt_lvl, timestmp, temp, press, hum, co, rms, ampx, frecx, ampy, frecy, ampz, frecz]

        for i in range(0, len(p3)):
            data_dict[p3[i]] = data3[i]

        return data_dict

    else:
        p4 = ["Batt_level", "Timestamp", "Temp", "Press", "Hum", "Co", "Acc_X", "Acc_Y", "Acc_Z", "Rgyr_X",
                "Rgyr_Y", "Rgyr_Z"]


        offset = calcsize("<H19s4i")
        batt_lvl, timestmp, temp, press, hum, co = unpack("<BLBLBf", data[:offset])

        step = calcsize("2000f")

        accx = unpack("2000f", data[offset:offset+step])
        accy = unpack("2000f", data[offset+step:offset+2*step])
        accz = unpack("2000f", data[offset+2*step:offset+3*step])
        rgyrx = unpack("2000f", data[offset+3*step:offset+4*step])
        rgyry = unpack("2000f", data[offset+4*step:offset+5*step])
        rgyrz = unpack("2000f", data[offset+5*step:offset+6*step])

        data4 = [batt_lvl, timestmp, temp, press, hum, co, accx, accy, accz, rgyrx, rgyry, rgyrz]
        
        for i in range(0, len(p4)):
            data_dict[p4[i]] = data4[i]

        return data_dict
      



# Probando si funciona el acceso a la base de datos desde otro archivo:

# Generación de los arreglos de 2000 floats que se usarán en los tests
# acc = numpy.random.uniform(-16.0, 16.0, size=(3, 2000))
# rgyr = numpy.random.uniform(-1000, 1000, size=(3, 2000))

# accx = []
# accy = []
# accz = []
# rgyrx = []
# rgyry = []
# rgyrz = []

# for i in range (0, 2000):
#     accx.append(acc[0][i])
#     accy.append(acc[1][i])
#     accz.append(acc[2][i])

#     rgyrx.append(rgyr[0][i])
#     rgyry.append(rgyr[1][i])
#     rgyrz.append(rgyr[2][i])


# # Headers y Datos de ejemplo para los protocolos del 0 al 3 y para el protocolo 4

# headers_datos = {"ID_device": 'Barry', "MAC": '2C:41:A1:27:09:57', "Transport_layer": '1', "ID_protocol": 2, "length": 51}

# headers_datos_4 = {"ID_device": 'Barry', "MAC": '2C:41:A1:27:09:57', "Transport_layer": '1', "ID_protocol": 4,"length": 51}

# insert_to_datos_values = {"Batt_level": 75, "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Temp": 15, "Press": 1100,
#                             "Hum": 55, "Co": 176, "RMS": 0.009, "Amp_X": 0.1, "Frec_X": 30.3, "Amp_Y": 0.05,
#                             "Frec_Y": 59.1, "Amp_Z": 0.009, "Frec_Z": 90.2}

# insert_to_datos_values4 = {"Batt_level": 75, "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Temp": 15, "Press": 1100,
#                             "Hum": 55, "Co": 176, "Acc_X": accx, "Acc_Y": accy, "Acc_Z": accz, "Rgyr_X":rgyrx, "Rgyr_Y":rgyry, "Rgyr_Z":rgyrz }


# Datos de ejemplo para insertar en la tabla de configuracion

insert_to_config = {"TCP_Port": 5432, "UDP_Port":8765, "Gyro_Sensibility":50, "Acc_Sensibility":27, "Gyro_SRate":99, "Acc_SRate":86, 
                    "Disc_Time":8, "Host_IP_Address":"127.0.0.0", "Wifi_SSID":"FCFM", "Wifi_Pass":"Pass12345"}

# Insertamos datos para un protocolo entre [0,3] y para protocolo 4. También insertamos información en la tabla de configuración

#insert_to_Datos(headers_datos, insert_to_datos_values)
#insert_to_Datos(headers_datos_4, insert_to_datos_values4)
#insert_to_Configuracion(headers_datos, insert_to_config)
#config = get_current_config()
#print(config)

#####################################

# Testeo de packing y unpacking

# Hacemos un packing con procolo 4
#packed = packing(headers_datos_4, insert_to_datos_values4)

# Hacemos un packing con procolo entre [0,3] (Modificar llave "ID_protocol" de la variable headers_datos)
# En este caso, está seteado ID_protocol = 2
# packed = packing(headers_datos, insert_to_datos_values)

# Printeamos la estructura obtenida

# print(packed)

# Unpacking

# headers, data = unpacking(packed)

# print(headers)
# print(data)