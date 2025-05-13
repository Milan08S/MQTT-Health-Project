## Acerca del Subscriber

El componente Subscriber es responsable de:

1. Conectarse a la base de datos PostgreSQL
2. Crear la tabla `health_readings` si no existe
3. Suscribirse al tema MQTT (`health/data`)
4. Recibir mensajes con datos de salud
5. Almacenar los datos en la base de datos

La tabla `health_readings` tiene la siguiente estructura:

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | SERIAL PRIMARY KEY | Identificador único |
| sensor_id | VARCHAR(50) | Identificador del sensor |
| temperature | FLOAT | Temperatura corporal |
| heart_rate | INTEGER | Frecuencia cardíaca |
| blood_pressure | VARCHAR(20) | Presión arterial |
| created_at | TIMESTAMP | Fecha y hora de registro |

## Verificación de Datos

Para verificar que los datos se están almacenando correctamente:

1. Conectarse a la base de datos PostgreSQL:
   ```bash
   docker exec -it postgres-db psql -U iotuser -d healthdata
   ```

2. Consultar los registros:
   ```sql
   SELECT * FROM health_readings ORDER BY created_at DESC LIMIT 10;
   ```

Alternativamente, si implementaste el servicio de monitoreo web, puedes acceder a él en tu navegador: http://localhost:5050

## Solución de Problemas

### Error de conexión a PostgreSQL

Si el subscriber no puede conectarse a PostgreSQL, verifica:

1. Que el nombre del host sea correcto en la variable `PG_HOST` (debe ser "postgres-db")
2. Que la base de datos esté en ejecución: `docker-compose ps db`
3. Que ambos contenedores estén en la misma red Docker: `docker network inspect mqtt-health-project_iot-net`

### Error de tabla inexistente

El subscriber debería crear automáticamente la tabla `health_readings` si no existe. Si enfrentas errores, puedes crear la tabla manualmente:

```bash
docker exec -it postgres-db psql -U iotuser -d healthdata -c "
CREATE TABLE IF NOT EXISTS health_readings (
    id SERIAL PRIMARY KEY,
    sensor_id VARCHAR(50),
    temperature FLOAT,
    heart_rate INTEGER,
    blood_pressure VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);"
```

### Advertencia de deprecación en paho-mqtt

Es normal ver una advertencia sobre API deprecada en paho-mqtt v2.0+. Para evitar esta advertencia, puedes actualizar el código a:

```python
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
```

