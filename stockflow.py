import threading
import time

from datos import NUM_CAJAS, NUM_TERMINALES, PEDIDOS, REPOSICIONES, STOCK_INICIAL

INVENTARIO = STOCK_INICIAL.copy()
semaforo = threading.Semaphore(NUM_TERMINALES)
condition = threading.Condition()


def caja(pedidos):
    for numero_pedido, producto, unidades in pedidos:
        procesar_pedido(numero_pedido, producto, unidades)


def almacen(pedidos):
    for numero_reposicion, producto, unidades in pedidos:
        procesar_reposicion(numero_reposicion, producto, unidades)


def procesar_pedido(numero_pedido, producto, unidades):
    nombre_caja = threading.current_thread().name

    with semaforo:
        print(f"{nombre_caja} obtiene un terminal ({numero_pedido})")
        time.sleep(0.1)

        with condition:
            while unidades > INVENTARIO[producto]:
                print(f"Pedido {numero_pedido} espera reposición de {producto}")
                condition.wait()
            INVENTARIO[producto] -= unidades

        print(f"Pedido {numero_pedido} realizado correctamente")
        print(f"{nombre_caja} libera un terminal ({numero_pedido})")


def procesar_reposicion(numero_reposicion, producto, unidades):
    time.sleep(0.5)

    with condition:
        INVENTARIO[producto] += unidades
        condition.notify_all()

    print(f"Reposición {numero_reposicion} añadió {unidades} unidades de {producto}")


if __name__ == "__main__":
    hilos = [
        threading.Thread(
            target=caja, args=(PEDIDOS[i::NUM_CAJAS],), name=f"Caja {i + 1}"
        )
        for i in range(NUM_CAJAS)
    ]
    hilos.append(threading.Thread(target=almacen, args=(REPOSICIONES,), name="Almacén"))

    for hilo in hilos:
        hilo.start()

    for hilo in hilos:
        hilo.join()

    print()
    print("Inventario inicial:", STOCK_INICIAL)
    print()
    print("Inventario final:", INVENTARIO)
