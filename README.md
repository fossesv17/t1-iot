## T3

### Integrantes

- David Parada
- Paula Ovalle
- Fabian Osses

---

## Correr Tarea
Como requisito inicial, se deben montar los distintos contenedores corriendo los comandos de docker. Esto buildeará 4 contenedores: Adminer, postgres, frontend y backend.

### Base de Datos
- Se logró implementar completamente la base de datos, pero no se logró conectar con la Raspi.
- Para correrla, dirigirse a codigo_rasp, correr el main del archivo "modelos.py". Esto creará las tablas Datos, Configuracion, Logs y Loss.
- Para obtener la configuración actual, se utiliza la función "get_current_config()".
- Utilizar las funciones para insertar datos en las respectivas tablas:
- insert_data_in_datos(...)
- insert_data_in_configuracion(...)
- insert_data_in_logs(...)
- insert_data_in_loss(...)

### Frontend
- Como explicamos en la Demo, esta parte se encuentra incompleta.
- Implementa únicamente la plantilla.
- Por diferentes motivos, no pudimos conectar correctamente el frontend. Por lo anterior, tampoco pudimos lograr que se actualizaran los datos en tiempo real.

### Raspi & ESP32
- No contamos con la implementación de BLE. Lo que logramos avanzar fue en Wifi.
- Las ESP logran generar los distintos datos que deben almacenarse. Sin embargo, no logramos establecer conexión con la base de datos, por lo que estos no pueden insertarse.
- La Raspi va alternando entre los distintos protocolos y transport layers, de manera automática.


## Comandos de docker


### Iniciar la base de datos

```bash
docker compose up -d
```

### Detener la base de datos

```bash
docker compose down
```

### Borrar la base de datos

```bash
docker compose down 
docker volume rm postgres_data_iot
```
