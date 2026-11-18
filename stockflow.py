import threading
import time

from datos_bis import (
    CANCELACIONES,
    NUM_CAJAS,
    NUM_REVISORES,
    NUM_TERMINALES,
    PEDIDOS,
    REPOSICIONES,
    STOCK_INICIAL,
    TIEMPO_COBRO,
    TIEMPO_REPOSICION,
)

ESTADOS = {pedido[0]: "PENDIENTE" for pedido in PEDIDOS}


class GestorInventario:
    def __init__(self, stock_inicial):
        self._inventario = stock_inicial.copy()
        self._lock = threading.RLock()
        self._condition = threading.Condition(self._lock)

    def consultar_stock(self, producto):
        with self._lock:
            return self._inventario[producto]

    def hay_stock(self, producto, unidades):
        with self._lock:
            return self.consultar_stock(producto) >= unidades

    def vender(self, numero_pedido, producto, unidades):
        with self._condition:
            while not self.hay_stock(producto, unidades):
                print(f"Pedido {numero_pedido} espera reposición de {producto}")
                self._condition.wait()
            self._inventario[producto] -= unidades
            print(f"Pedido {numero_pedido} realizado correctamente")

            for ele in ESTADOS:
                if ele == numero_pedido:
                    if ESTADOS[ele] != "CANCELADO":
                        ESTADOS[ele] = "COMPLETADO"

    def reponer(self, producto, unidades):
        with self._condition:
            self._inventario[producto] += unidades
            self._condition.notify_all()

    def cancelar(self, numero_pedido):
        with self._condition:
            for ele in ESTADOS:
                if ele == numero_pedido:
                    if ESTADOS[ele] == "PENDIENTE":
                        ESTADOS[ele] = "CANCELADO"

    def productos(self):
        with self._lock:
            return list(self._inventario)

    def copia(self):
        with self._lock:
            return self._inventario.copy()


gestor = GestorInventario(STOCK_INICIAL)
semaforo = threading.Semaphore(NUM_TERMINALES)
barrera = threading.Barrier(NUM_REVISORES)


def caja(pedidos):
    for numero_pedido, producto, unidades in pedidos:
        procesar_pedido(numero_pedido, producto, unidades)


def almacen(pedidos):
    for numero_reposicion, producto, unidades in pedidos:
        procesar_reposicion(numero_reposicion, producto, unidades)


def revisor(productos):
    nombre = threading.current_thread().name

    for producto in productos:
        stock = gestor.consultar_stock(producto)
        if stock >= 0:
            estado = "OK"
        else:
            estado = "ERROR: stock negativo"
        print(f"{nombre} revisa {producto}: {stock} unidades ({estado})")

    time.sleep(0.5)
    print(f"{nombre} ha terminado y espera en la barrera")
    barrera.wait()
    print(f"{nombre} supera la barrera")


def procesar_pedido(numero_pedido, producto, unidades):
    nombre_caja = threading.current_thread().name

    with semaforo:
        print(f"{nombre_caja} obtiene un terminal ({numero_pedido})")
        time.sleep(TIEMPO_COBRO)

        gestor.vender(numero_pedido, producto, unidades)

        print(f"{nombre_caja} libera un terminal ({numero_pedido})")


def procesar_reposicion(numero_reposicion, producto, unidades):
    time.sleep(TIEMPO_REPOSICION)

    gestor.reponer(producto, unidades)

    print(f"Reposición {numero_reposicion} añadió {unidades} unidades de {producto}")


def cancelar(cancelaciones):
    for numero_cancelacion, pedido, tiempo in cancelaciones:
        procesar_cancelacion(numero_cancelacion, pedido, tiempo)


def procesar_cancelacion(numero_cancelacion, numero_pedido, tiempo):
    time.sleep(tiempo)

    gestor.cancelar(numero_pedido)

    print(f"Cancelación {numero_cancelacion} canceló el pedido {numero_pedido}")

def resumen(diccionario):
    procesados = 0
    cancelados = 0
    for ele in diccionario:
        if diccionario[ele] == "COMPLETADO":
            procesados += 1
        elif diccionario[ele] == "CANCELADO":
            cancelados += 1

    print(f"""
===== RESUMEN =====
Cantidad de pedidos procesados: {procesados}
Cantidad de pedidos cancelados: {cancelados}""")



if __name__ == "__main__":
    hilos = [
        threading.Thread(
            target=caja, args=(PEDIDOS[i::NUM_CAJAS],), name=f"Caja {i + 1}"
        )
        for i in range(NUM_CAJAS)
    ]
    hilos.append(threading.Thread(target=almacen, args=(REPOSICIONES,), name="Almacén"))

    hilos.append(
        threading.Thread(target=cancelar, args=(CANCELACIONES,), name="Cancelaciones")
    )

    for hilo in hilos:
        hilo.start()

    for hilo in hilos:
        hilo.join()

    productos = gestor.productos()
    revisores = [
        threading.Thread(
            target=revisor,
            args=(productos[i::NUM_REVISORES],),
            name=f"Revisor {i + 1}",
        )
        for i in range(NUM_REVISORES)
    ]

    for hilo in revisores:
        hilo.start()

    for hilo in revisores:
        hilo.join()

    print()
    print("===== IINVENTARIO INICIAL =====\n", STOCK_INICIAL)
    print()
    print("===== INVENTARIO FINAL =====\n", gestor.copia())
    print()
    resumen(ESTADOS)
