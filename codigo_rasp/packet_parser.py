from struct import unpack, pack
from pickle import dumps, loads
import datetime
import traceback
from modelos import * 

# Documentación struct unpack,pack :https://docs.python.org/3/library/struct.html#

'''
-headerToDict: Transforma los headers en un diccionario con la informacion correspondiente.
-protocolUnpack: desempaqueta los datos del mensaje
-dataToDict: Transforma el area de datos en un diccionario con los datos del mensaje
-parseData: Utiliza dataToDict para obtener los datos y luego los almacena en la base de datos
'''

def response(ID_protocol:int, transport_layer:int):
    return pack("<BB", ID_protocol,transport_layer)

def getHeader(packet):
    header = packet[:12]
    header = headerToDict(header)
    print(header)
    return header

def headerToDict(data):
    ID_Device, M1, M2, M3, M4, M5, M6, transport_layer, protocol, len_msg = unpack("<2B6BBB2B", data)
    MAC = ".".join([hex(x)[2:] for x in [M1, M2, M3, M4, M5, M6]])
    return {"ID_device":ID_Device, "MAC":MAC, "ID_protocol":protocol, "Transport_layer":transport_layer, "length":len_msg}

def getData(packet):
    d1 = packet[0]
    dictData = d1 #unpack("<B",d1)
    return dictData

def parseData(header, packet):
    dictData = dataToDict(header["ID_protocol"], packet)
    if dictData is not None:
        # Falta definir la funcion saveData en los modelos
        saveData(header, dictData)
        print(dictData)
        
    return None if dictData is None else {**header, **dictData}

def protocolUnpack(protocol:int, data):
    protocol_unpack = ["<B", "<B4B", "<B4BB4BBf", "<B4BB4BBffffffff", "<B4BB4BBf2000f2000f2000f2000f2000f2000f"]
    return unpack(protocol_unpack[protocol], data)


def dataToDict(protocol:int, data):
    if protocol not in [0, 1, 2, 3, 4]:
        print("Error: protocol doesnt exist")
        return None
    
    def protocolFunc(protocol, keys):
        def p(data):
            unp = protocolUnpack(protocol, data)
            data_dict = {}
            for (key,val) in zip(keys,unp):
                if key == "Timestamp":
                    data_dict[key] = datetime.datetime.now()
                elif key in ["Acc_X", "Acc_Y", "Acc_Z", "Rgyr_X", "Rgyr_Y", "Rgyr_Z"]:
                    data_dict[key] = dumps(val)
                else:
                    data_dict[key] = val
            return data_dict
        return p
    
    p0 = ["Batt_level"]
    p1 = ["Batt_level", "Timestamp"]
    p2 = ["Batt_level", "Timestamp", "Temp", "Press", "Hum", "Co"]
    p3 = ["Batt_level", "Timestamp", "Temp", "Press", "Hum", "Co", "RMS", "Amp_X", "Frec_X", "Amp_Y", "Frec_Y", "Amp_Z", "Frec_Z"]
    p4 = ["Batt_level", "Timestamp", "Temp", "Press", "Hum", "Co", "Acc_X", "Acc_Y", "Acc_Z", "Rgyr_X", "Rgyr_Y", "Rgyr_Z"]

    p = [p0, p1, p2, p3, p4]

    try:
        return protocolFunc(protocol, p[protocol])(data)
    except Exception:
        print("Data unpacking Error:", traceback.format_exc())
        return None


