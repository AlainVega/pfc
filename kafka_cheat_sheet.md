## Topics

### Crear un topic
kafka-topics.sh --create \
  --topic mi_tema \
  --bootstrap-server localhost:9092 \
  --partitions 1 \
  --replication-factor 1

### Listar todos los topics
kafka-topics.sh --list --bootstrap-server localhost:9092

### Describir un topic
kafka-topics.sh --describe \
  --topic mi_tema \
  --bootstrap-server localhost:9092

### Eliminar un topic
kafka-topics.sh --delete \
  --topic mi_tema \
  --bootstrap-server localhost:9092

## Producer y Consumer

### Producer CLI
kafka-console-producer.sh \
  --topic mi_tema \
  --bootstrap-server localhost:9092

### Consumer CLI
kafka-console-consumer.sh \
  --topic mi_tema \
  --bootstrap-server localhost:9092 \
  --from-beginning

## Offsets y Consumers

### Ver offsets y estado de grupos de consumidores
kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --list

### Describir un grupo de consumidores
kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --describe --group grupo1

### Resetear offsets de un grupo (ejemplo: volver al inicio)
kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --group grupo1 \
  --topic mi_tema \
  --reset-offsets --to-earliest --execute

## Brokers

### Probar si el broker responde (listar topics)
kafka-topics.sh --list --bootstrap-server localhost:9092

## Enviar mensajes desde un archivo
kafka-console-producer.sh \
  --topic mi_tema \
  --bootstrap-server localhost:9092 < mensajes.txt

# Guardar mensajes en un archivo
kafka-console-consumer.sh \
  --topic mi_tema \
  --bootstrap-server localhost:9092 \
  --from-beginning > salida.txt

# Crear 10 mensajes de prueba
seq 10 | kafka-console-producer.sh \
  --topic mi_tema \
  --bootstrap-server localhost:9092

# Ver versión de Kafka
kafka-topics.sh --version
