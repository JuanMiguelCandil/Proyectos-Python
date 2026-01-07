import requests
import sys

url_base = "http://localhost:8080/api/get/"

municipio = " ".join(sys.argv[1:])

url = f"{url_base}{municipio}"
try:
    resp = requests.get(url)
    resp.raise_for_status()
    datos = resp.json()
    if "Población" in datos:
        print(datos["Población"])
    else:
        print("Formato inesperado de respuesta:", datos)
except Exception as e:
    print("No se ha encontrado el municipio:", e)