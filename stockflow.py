import threading
import time

import requests

from datos import NUM_CAJAS, PEDIDOS, STOCK_INICIAL

INVENTARIO = STOCK_INICIAL.copy()


def crear_pedidos(numero_pedido, producto, unidades):
    if producto not in INVENTARIO or unidades > INVENTARIO[producto]:
        print(f"No quedan existencias de {producto}")
    else:
        INVENTARIO[producto] -= unidades


if __name__ == "__main__":
    hilos = []

    for pedido in PEDIDOS:
        tanda = [
            threading.Thread(target=crear_pedidos, args=pedido)
            for _ in range(NUM_CAJAS)
        ]
        hilos.append(tanda)

    for tanda in hilos:
        for hilo in tanda:
            hilo.start()

    for tanda in hilos:
        for hilo in tanda:
            hilo.join()

    print()
    print("Inventario inicial:", STOCK_INICIAL)
    print()
    print("Inventario final:", INVENTARIO)
