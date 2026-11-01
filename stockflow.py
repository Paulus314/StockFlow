import threading
import time

from datos import NUM_CAJAS, NUM_TERMINALES, PEDIDOS, STOCK_INICIAL

INVENTARIO = STOCK_INICIAL.copy()
lock = threading.Lock()
semaforo = threading.Semaphore(NUM_TERMINALES)


def caja(pedidos):
    for numero_pedido, producto, unidades in pedidos:
        procesar_pedido(numero_pedido, producto, unidades)


def procesar_pedido(numero_pedido, producto, unidades):
    nombre_caja = threading.current_thread().name

    with semaforo:
        print(f"{nombre_caja} obtiene un terminal ({numero_pedido})")
        time.sleep(0.5)
        with lock:
            if producto not in INVENTARIO or unidades > INVENTARIO[producto]:
                vendido = False
            else:
                INVENTARIO[producto] -= unidades
                vendido = True
        print(f"{nombre_caja} libera un terminal ({numero_pedido})")

    if vendido:
        print(f"Pedido {numero_pedido} realizado correctamente")
    else:
        print(
            f"Pedido {numero_pedido} no se ha podido realizar por falta de existencias de {producto}"
        )


if __name__ == "__main__":
    hilos = [
        threading.Thread(
            target=caja, args=(PEDIDOS[i::NUM_CAJAS],), name=f"Caja {i + 1}"
        )
        for i in range(NUM_CAJAS)
    ]

    for hilo in hilos:
        hilo.start()

    for hilo in hilos:
        hilo.join()

    print()
    print("Inventario inicial:", STOCK_INICIAL)
    print()
    print("Inventario final:", INVENTARIO)
