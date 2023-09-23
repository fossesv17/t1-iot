
import struct # Libreria muy util para codificar y decodificar datos


"""

--- Packing en C ---



char * pack(int packet_id, float value_float, char * text) {
    char * packet = malloc(12 + strlen(text));
    memcpy(packet, &packet_id, 4);
    memcpy(packet + 4, &value_float, 4);
    memcpy(packet + 8, &largo_text, 4);
    memcpy(packet + 12, text, largo_text);
    return packet;
}

//Luego mandan el paquete por el socket


--- Unpacking en C ---


void unpack(char * packet) {
    int packet_id;
    float value_float;
    int largo_text;
    char * text;

    memcpy(&packet_id, packet, 4);
    memcpy(&value_float, packet + 4, 4);
    memcpy(&largo_text, packet + 8, 4);

    text = malloc(largo_text + 1); // +1 for the null-terminator
    if (text == NULL) {
        // Handle memory allocation failure
        return;
    }
    
    memcpy(text, packet + 12, largo_text);
    text[largo_text] = '\0'; // Null-terminate the string

    printf("Packet ID: %d\n", packet_id);
    printf("Float Value: %f\n", value_float);
    printf("Text: %s\n", text);

    free(text); 
}


"""


def pack(packet_id: int, device_mac: str, transport_layer: str, id_protocol: int, length: int, body: str) -> bytes:
    body = body.encode("utf-8")
    device_mac = device_mac.encode()
    transport_layer = transport_layer.encode("utf-8")
    largo_body = len(body)
    """
     '<' significa que se codifica en little-endian
     'h' significa que el dato es un short de 2 bytes
     'c' significa que el dato es un char de 1 bytes
     '{}s'.format(largo_body) (ej: 10s para un string de largo 10) significa que el string tiene largo variable,

    

    """

    return struct.pack('<h6s1sbh{}s'.format(largo_body), packet_id, device_mac, transport_layer, id_protocol, length, body)


def unpack(packet: bytes) -> list:
    packet_id, device_mac, transport_layer, id_protocol, length = struct.unpack('<h6s1sbh', packet[:12])
    # length = headers + body -> body = lenght - headers
    largo_body = length - 12

    # Body como string
    body = struct.unpack('<{}s'.format(largo_body), packet[12:])[0]

    # Variable donde se almacena la data
    data = []

    if id_protocol==0:

        # Cortamos el mensaje de acuerdo a los datos que trae
        # Batt_lvl -> 1byte
        batt_lvl = int(body.decode("utf-8"))

        data.append(batt_lvl)

        
    elif id_protocol==1:

        # 1 + 4 = 5
        body = body[:5]

        # Obtenemos cada dato por separado
        batt_lvl = int(body.decode("utf-8")[0])

        # Falta definir formato del timestap
        timestap = body.decode("utf-8")[1:5]

        # Los agregamos a la data para retornar
        data.append(batt_lvl)
        data.append(timestap) 

    elif id_protocol==2:

        # 1 + 4 + 1 + 4 + 1 + 4 = 15
        body = body[:15]

        # Obtenemos cada dato por separado
        batt_lvl = int(body.decode("utf-8")[0])
        timestap = body.decode("utf-8")[1:5]
        temp = int(body.decode("utf-8")[5])
        press = int(body.decode("utf-8")[6:10])
        hum = int(body.decode("utf-8")[10])
        co = float(body.decode("utf-8")[11:15])

        # Los agregamos a la data para retornar
        data.append(batt_lvl)
        data.append(timestap)
        data.append(temp)
        data.append(press)
        data.append(hum)
        data.append(co)
    
    elif id_protocol==3:

        # 15 + 4x7 = 15 + 28 = 43
        body = body[:43]

        # Obtenemos cada dato por separado
        batt_lvl = int(body.decode("utf-8")[0])
        timestap = body.decode("utf-8")[1:5]
        temp = int(body.decode("utf-8")[5])
        press = int(body.decode("utf-8")[6:10])
        hum = int(body.decode("utf-8")[10])
        co = float(body.decode("utf-8")[11:15])

        rms = float(body.decode("utf-8")[15:19])
        amp_x = float(body.decode("utf-8")[19:23])
        frec_x = float(body.decode("utf-8")[23:27])
        amp_y = float(body.decode("utf-8")[27:31])
        frec_y = float(body.decode("utf-8")[31:35])
        amp_z = float(body.decode("utf-8")[35:39])
        frec_z = float(body.decode("utf-8")[39:43])

        # Los agregamos a la data para retornar
        data.append(batt_lvl)
        data.append(timestap)
        data.append(temp)
        data.append(press)
        data.append(hum)
        data.append(co)
        data.append(rms)
        data.append(amp_x)
        data.append(frec_x)
        data.append(amp_y)
        data.append(frec_y)
        data.append(amp_z)
        data.append(frec_z)


    elif id_protocol==4:

        # 15 + 48000 = 48015
        body = body[:48015] 

        # Obtenemos cada dato por separado
        batt_lvl = int(body.decode("utf-8")[0])
        timestap = body.decode("utf-8")[1:5]
        temp = int(body.decode("utf-8")[5])
        press = int(body.decode("utf-8")[6:10])
        hum = int(body.decode("utf-8")[10])
        co = float(body.decode("utf-8")[11:15])

        acc_x = body[15:8015].decode("utf-8")
        acc_y = body[8015:16015].decode("utf-8")
        acc_z = body[16015:24015].decode("utf-8")
        rgyr_x = body[24015:32015].decode("utf-8")
        rgyr_y = body[32015:40015].decode("utf-8")
        rgyr_z = body[40015:48015].decode("utf-8")

        # Los agregamos a la data para retornar
        data.append(batt_lvl)
        data.append(timestap)
        data.append(temp)
        data.append(press)
        data.append(hum)
        data.append(co)
        data.append(acc_x)
        data.append(acc_y)
        data.append(acc_z)
        data.append(rgyr_x)
        data.append(rgyr_y)
        data.append(rgyr_z)

    else:
        print("Protocolo Desconocido :(\n")
    

    return [packet_id, device_mac, transport_layer, id_protocol, length, data]



if __name__ == "__main__":
    #mensage = pack(1, 3.20, "Hola mundo")
    #print(mensage)
    #print(unpack(mensage))


    print("Ejemplo Protocolo 0")

    msg = pack(1,"123456","0",0, 13, "8")
    print(msg)
    print(unpack(msg))

    print("Ejemplo Protocolo 1")

    msg1 = pack(1,"123456","0",1, 17, "01234")
    print(msg1)
    print(unpack(msg1))

    print("Ejemplo Protocolo 2")

    msg2 = pack(1,"123456","0",2, 27, "0123484534212.1")
    print(msg2)
    print(unpack(msg2))

    print("Ejemplo Protocolo 3")

    msg3 = pack(1,"123456","0",3, 55, "0123484534212.14321123487655678123456781234")
    print(msg3)
    print(unpack(msg3))


