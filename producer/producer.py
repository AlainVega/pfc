from confluent_kafka import Producer
import json
import time
import socket

conf = {
    'bootstrap.servers': 'kafka:9092', 
    'client.id': socket.gethostname()
}

producer = Producer(conf)

topic = "python_test" 

def delivery_report(err, msg):
    """ Callback de confirmación de envío """
    if err is not None:
        # print(f"Error al entregar mensaje: {err}") # Lo comentamos para no saturar el log
        pass
    else:
        # print(f"Mensaje entregado a {msg.topic()} [{msg.partition()}]") # Lo comentamos para no saturar el log
        pass

print("Iniciando producción de mensajes en el topic:", topic)

for i in range(10000):
    
    mensaje = {"id": i, "timestamp": int(time.time() * 1000), "texto": f"mensaje numero {i} a kafka", "valor": i % 100}
    
    producer.produce(topic, value=json.dumps(mensaje).encode('utf-8'), callback=delivery_report)
    
    time.sleep(1)
    producer.poll(0)  # procesa eventos de entrega

# Asegurarse que todos los mensajes se envíen antes de salir:
print("Esperando a que se envíen todos los mensajes pendientes...")
producer.flush()
print("Producción de mensajes finalizada.")