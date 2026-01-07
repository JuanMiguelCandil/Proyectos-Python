import socket
import random

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def mostrar_palitos(n):
    return '|' * n

def main():
    print("JUEGO DE LOS PALITOS")
    print("1. Servidor")
    print("2. Cliente")
    modo = input("Elige de que quieres jugar (1/2): ")

    if modo == "1":
        iniciar_servidor()
    elif modo == "2":
        iniciar_cliente()
    else:
        print("Opción no válida.")

def iniciar_servidor():
    host = get_ip()
    port = 6767

    print("\nTu IP es " + str(host) + ". Dásela al cliente para que se conecte.")
    print("Esperando conexión del cliente")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    conn, addr = s.accept()
    print("Conectado con " + str(addr))

    msg = conn.recv(1024).decode()
    if msg != "EMPEZAMOS":
        print("Mensaje inesperado. Cerrando conexión.")
        conn.close()
        return

    palitos = random.randint(10, 20)
    print("Número inicial de palitos: " + str(palitos))
    conn.send(str(palitos).encode())

    while True:
        palitos = int(conn.recv(1024).decode())
        if palitos <= 0:
            print("¡Has ganado! El cliente se quedó con el último palito.")
            break
        print("\nPalitos actuales: " + mostrar_palitos(palitos)  + str(palitos))

        quitar = 0
        while quitar not in [1, 2, 3] or quitar > palitos:
            try:
                quitar = int(input("¿Cuántos palitos quieres quitar (1-3)? "))
            except ValueError:
                quitar = 0

        palitos -= quitar
        if palitos <= 0:
            print("¡Has perdido! Te quedaste con el último palito.")
            conn.send(str(0).encode())
            break

        conn.send(str(palitos).encode())

    conn.close()
    s.close()

def iniciar_cliente():
    host = input("Introduce la IP del servidor: ")
    port = 6767

    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        c.connect((host, port))
    except Exception as e:
        print("No se pudo conectar al servidor:", e)
        return

    c.send("EMPEZAMOS".encode())

    palitos = int(c.recv(1024).decode())
    print("\nComenzamos con " + str(palitos) + " palitos.")

    while True:
        print("\nPalitos actuales: " + mostrar_palitos(palitos) + str(palitos))

        quitar = 0
        while quitar not in [1, 2, 3] or quitar > palitos:
            try:
                quitar = int(input("¿Cuántos palitos quieres quitar (1-3)? "))
            except ValueError:
                quitar = 0

        palitos -= quitar
        if palitos <= 0:
            print("¡Has perdido! Te quedaste con el último palito.")
            c.send(str(0).encode())
            break

        c.send(str(palitos).encode())

        palitos = int(c.recv(1024).decode())
        if palitos <= 0:
            print("¡Has ganado! El servidor se quedó con el último palito.")
            break

    c.close()

if __name__ == "__main__":
    main()
