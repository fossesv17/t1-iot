import asyncio
from bleak import BleakClient


def convert_to_128bit_uuid(short_uuid):
    # Usada para convertir un UUID de 16 bits a 128 bits
    # Los bits fijos son utilizados para BLE ya que todos los UUID de BLE son de 128 bits
    # y tiene este formato: 0000XXXX-0000-1000-8000-00805F9B34FB
    base_uuid = "00000000-0000-1000-8000-00805F9B34FB"
    short_uuid_hex = "{:04X}".format(short_uuid)
    return base_uuid[:4] + short_uuid_hex + base_uuid[8:]


ADDRESS = "24:0A:C4:1C:99:7E"
CHARACTERISTIC_UUID = convert_to_128bit_uuid(0xFF01) # Busquen este valor en el codigo de ejemplo de esp-idf


async def main(ADDRESS):
    async with BleakClient(ADDRESS) as client:
        char_value = await client.read_gatt_char(CHARACTERISTIC_UUID)
        print("Characterisic A {0}".format("".join(map(chr, char_value))))
        # Luego podemos escribir en la caracteristica
        data = 'Hello World!'.encode()
        await client.write_gatt_char(CHARACTERISTIC_UUID, data)

asyncio.run(main(ADDRESS))