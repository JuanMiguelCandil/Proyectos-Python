import requests
import sys
import json

url_help = "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies.json"
url_base = "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies"
datos_help = requests.get(url_help)

json_help = datos_help.json()

if (len(sys.argv) != 2) and (len(sys.argv) != 6):
    print("No has introducido los parametros correctos")
    sys.exit()

try:
    if sys.argv[1] == "-help":
        print("Debes usar la siguiente sintaxis: ")
        print("'-from' '(moneda que quieras cambiar)' '-to' '(moneda a la que quieres realizar el cambio)' 'cantidad'")
        print("Aquí tienes una lista con todas las monedas que puedes realizar el cambio:")
        print(json.dumps(json_help, indent=2, ensure_ascii=False))
        sys.exit()
    elif sys.argv[1] == "-from" and sys.argv[3] == "-to":
        moneda_origen = sys.argv[2]
        moneda_destino = sys.argv[4]
        cantidad = float(sys.argv[5])
        if moneda_origen not in json_help:
            print("La moneda que quiere cambiar no existe.")
            sys.exit()
        if moneda_destino not in json_help:
            print("La moneda a la que desea cambiar no existe.")
            sys.exit()
                
        url_origen = f"{url_base}/{moneda_origen}.json"
        datos_origen = requests.get(url_origen).json()

        if moneda_destino not in datos_origen[moneda_origen]:
            print("No se puede comvertir a la moneda: ", moneda_destino)
            sys.exit()
        
        tasa = datos_origen[moneda_origen][moneda_destino]
        resultado = cantidad * tasa

        print(f"{cantidad} {moneda_origen} = {resultado:.2f} {moneda_destino}")

except Exception as e:
    print("Error", e)