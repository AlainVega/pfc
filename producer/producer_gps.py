# %%
from confluent_kafka import Producer
import json
import time
import geopandas as gpd
import numpy as np
import os
import threading
import socket

conf = {
    'bootstrap.servers': 'kafka:9092', 
    'client.id': socket.gethostname()
}

producer = Producer(conf)

topic = "gps_test"

# %%
file_path = os.path.abspath(os.path.join(os.path.abspath(__file__), '../Itinerarios de Buses Metropolitanos.geojson'))

gdf = gpd.read_file(file_path, driver='geojson')

# %%

# Número de puntos GPS a simular:
n_points = 100

def enviar_ubicacion_colectivo(linea: str, id_: str, empresa: str, geometry, n_points=5):
    """ Función para simular datos GPS de buses y enviarlos a Kafka """

    # Reproyectamos a metros (UTM 21S para Paraguay):
    line_proj = gpd.GeoSeries([geometry], crs="EPSG:4326").to_crs(epsg=32721).iloc[0]
    # Interpolamos puntos equidistantes (/2 porque la ruta es ida y vuelta):
    points_proj = [line_proj.interpolate(d) for d in np.linspace(0, line_proj.length / 2, n_points)]
    # Convertir de vuelta a lat/lon (EPSG:4326):
    points = gpd.GeoSeries(points_proj, crs="EPSG:32721").to_crs(epsg=4326)

    # Enviar cada punto como un mensaje Kafka
    for idx, pt in enumerate(points):
        mensaje = {
            "linea": linea,
            "id": str(id_),
            "empresa": empresa,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "lat": pt.y,
            "lon": pt.x,
            "sequence": idx
        }

        producer.produce(topic, value=json.dumps(mensaje)) # enviar mensaje
        producer.poll(0) # procesa callbacks
        time.sleep(5)  # velocidad de simulación

# %%
# Crear y lanzar un hilo por cada colectivo
threads = []

for (linea, id_), grupo in gdf.groupby(["linea", "id"]):
    empresa = grupo.iloc[0].get("empresa", "Desconocida")
    geometry = grupo.iloc[0]["geometry"]
    
    t = threading.Thread(target=enviar_ubicacion_colectivo, args=(linea, id_, empresa, geometry, n_points))
    threads.append(t)
    t.start()

# Esperar a que terminen todos
for t in threads:
    t.join()

# Asegurar que todos los mensajes se envíen
producer.flush()
# %%
