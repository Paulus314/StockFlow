import threading

from datos import NUM_CAJAS, PEDIDOS, STOCK_INICIAL

INVENTARIO = STOCK_INICIAL.copy()
lock = threading.Lock()


def caja(pedidos):
    for numero_pedido, producto, unidades in pedidos:
        procesar_pedido(numero_pedido, producto, unidades)


def procesar_pedido(numero_pedido, producto, unidades):
    with lock:
        if producto not in INVENTARIO or unidades > INVENTARIO[producto]:
            vendido = False
        else:
            INVENTARIO[producto] -= unidades
            vendido = True

    if vendido:
        print(f"Pedido {numero_pedido} realizado correctamente")
    else:
        print(
            f"Pedido {numero_pedido} no se ha podido realizar por falta de existencias de {producto}"
        )


if __name__ == "__main__":
    hilos = []

    for i in range(NUM_CAJAS):
        hilo = threading.Thread(target=caja, args=(PEDIDOS[i::NUM_CAJAS],))
        hilos.append(hilo)

    for hilo in hilos:
        hilo.start()

    for hilo in hilos:
        hilo.join()

    print()
    print("Inventario inicial:", STOCK_INICIAL)
    print()
    print("Inventario final:", INVENTARIO)
