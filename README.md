# StockFlow

La actividad consiste en una simulación de una tienda. Esta tienda dispone de varias cajas que procesan pedidos de clientes mientras el almacén realiza reposiciones. Todos trabajan sobre un mismo inventario. Cuando varias cajas venden al mismo tiempo o cuando una reposición coincide con una venta, distintos hilos pueden intentar leer o modificar el mismo stock.

## Ejecutar la aplicación

Para ejecutar la aplicación tiene que estar instalado Python en el equipo y hay que escribir en la terminal el comando python stockflow.py desde la carpeta donde se ubica el archivo,otra opción es darle al play de VS Code si tenemos instalado el intérprete de Python.

## Estructura de archivos

La estructura de archivos es la siguiente: un archivo datos.py con los datos iniciales que vamos a usar (este archivo viene dado por el profesor), el archivo stockflow.py donde está el conjunto del ejercicio, este README.md con la explicación del programa y un .gitignore.

## Condición de carrera inicial (sección crítica)

La condición de carrera se da cuando varios hilos acceden a la vez a la misma parte del programa, en este caso sería cuando varias cajas acceden al mismo producto a la vez.

La sección crítica en este programa se sitúa en la línea que descuenta elementos del inventario: self._inventario[producto] -= unidades. Eso es algo que no deberían de hacerlo varios hilos a la vez.

## Uso y finalidad de Lock, RLock, Semaphore, Condition y Barrier

Lock en este programa es necesario para proteger la sección crítica del programa y que cada hilo actúe sobre esa parte de forma individual (uno a la vez). Se sustituyó por RLock.

Para este diseño es necesario el RLock porque usando solamente Lock el programa se bloquearía. esto se debe a que un hilo no puede acceder si un Lock está bloqueado, mientras que con RLock un hilo diferente si puede acceder aunque ya haya un bloqueo.

Semaphore sirve para limitar el acceso a una parte del programa, en este caso tenemos uno que limita en 3 el número de cajas que pueden acceder a las terminales de pago a la vez.

Condition sirve para que una parte del programa se ejecute si y solo si se cumple una condición específica, en nuestro caso lo usamos para permitir procesar el pedido solamente si hay stock del producto.

Barrier sirve para poner una barrera que limite avanzar a los hilos hasta que esa barrera se cumpla, nosotros lo usamos para simular el trabajo de unos revisores. Los cuales se esperan entre sí hasta que todos terminen el trabajo.

## Posible deadlock

Un deadlock ocurre cuando varios hilos esperan recursos que tienen otros y ninguno puede continuar. En este programa no existe deadlock, el riesgo está en modificar el orden de ejecución ya que una caja que espera una reposición con mantiene su terminal ocupado y si otra caja necesita ese terminal para seguir avanzando el programa se bloquearía.
