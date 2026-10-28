import threading
import time

import requests

from datos import STOCK_INICIAL
from datos import PEDIDOS


INVENTARIO = STOCK_INICIAL.copy()
NUM_CAJAS = []


def crear_pedidos(numero_pedido, producto, unidades):
    if producto not in INVENTARIO or unidades > INVENTARIO[producto]:
        print(f"No quedan existencias de {producto}")
    else:
        INVENTARIO[producto] -= unidades


if __name__ == "__main__":
    for pedido in PEDIDOS:
        hilo = threading.Thread(target=crear_pedidos, args=pedido)
        NUM_CAJAS.append(hilo)

    for hilo in NUM_CAJAS:
        hilo.start()

    for hilo in NUM_CAJAS:
        hilo.join()

    print()
    print("Inventario inicial:", STOCK_INICIAL)
    print()
    print("Inventario final:", INVENTARIO)
