# StockFlow

## Fase 1 (sección crítica)

    La sección crítica en este programa se sitúa en la líne 15, esa parte es donde el programa descuenta unidades del stock del inventario y no deberían de hacerlo varios hilos a la vez.

## Fase 6 (RLock)

    Para este diseño es necesario el RLock porque usando solamente Lock el programa se bloquearía.