import threading
import time

import requests

from datos import STOCK_INICIAL
from datos import PEDIDOS


INVENTARIO_INICIAL = STOCK_INICIAL
INVENTARIO_FINAL = STOCK_INICIAL
NUM_CAJAS = []


def crear_pedidos(numero_pedido, producto, unidades):
    if producto not in INVENTARIO_FINAL or unidades > INVENTARIO_FINAL[producto]:
        print(f"No quedan existencias de {producto}")
    else:
        INVENTARIO_FINAL[producto] -= unidades


if __name__ == "__main__":
    for pedido in PEDIDOS:
        hilo = threading.Thread(target=crear_pedidos, args=pedido)
        NUM_CAJAS.append(hilo)

    for hilo in NUM_CAJAS:
        hilo.start()

    for hilo in NUM_CAJAS:
        hilo.join()

    print()
    print("Inventario inicial:", INVENTARIO_INICIAL)
    print()
    print("Inventario final:", INVENTARIO_FINAL)
