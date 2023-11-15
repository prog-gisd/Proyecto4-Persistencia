<img  align="left" width="150" style="float: left;" src="https://www.upm.es/sfs/Rectorado/Gabinete%20del%20Rector/Logos/UPM/CEI/LOGOTIPO%20leyenda%20color%20JPG%20p.png">

<br/><br/>

# Proyecto 4 - Persistencia


## Contenido

- [Requisitos previos](#requisitos-previos)
- [Objetivos](#objetivos)
- [Introducción](#introducción)
- [Actividades del proyecto](#actividades-del-proyecto)
  - [0. Descarga del proyecto](#0-descarga-del-proyecto)
  - [1. Persistencia básica](#1-persistencia-básica)
  - [2. Serialización en texto plano](#2-serialización-en-texto-plano)
  - [3. Clase Almacén](#3-clase-almacén)
  - [4. Habilidad lista de la compra con excepciones](#4-habilidad-lista-de-la-compra-con-excepciones)
  - [5. Habilidad lista de la compra con persistencia](#5-habilidad-lista-de-la-compra-con-persistencia)
  - [6. Actividades opcionales](#6-actividades-opcionales)
- [Entrega del proyecto](#entrega-del-proyecto)
- [Anexos](#anexos)
  - [Evaluación](#evaluación)
  - [Convenciones](#convenciones)
- [Enlaces](#enlaces)

## Requisitos previos

Disponer de una versión de Python igual o superior a 3.10, y del entorno de desarrollo Visual Studio Code. Además, se deben haber realizado los proyectos anteriores (1 a 3).

En la realización de este proyecto se ponen en práctica conceptos abordados en los temas del 1 al 8 de la asignatura.

## Objetivos

-   Uso interactivo del intérprete de Python (REPL)
-   Uso básico de un IDE (Visual Studio Code) para desarrollar y ejecutar código
-   Uso de persistencia básica en disco
-   Uso de diferentes formatos de serialización (texto plano, JSON, Pickle)
-   Uso de excepciones
-   Refuerzo del uso de clases para encapsular estado y comportamiento.
-   Refuerzo de conceptos básicos de ingenierı́a de software como interfaces

## Introducción

En el proyecto anterior desarrollamos un sistema funcional con un conjunto de habilidades y menús para poder presentar esas habilidades a los usuarios.
Sin embargo, tenı́amos la limitación de que el estado de las habilidades (p.e., la lista de la compra) no se guarda entre ejecuciones.

En este proyecto implementaremos persistencia en nuestras habilidades.
Buscamos poder guardar el estado de nuestra aplicación entre ejecuciones.
El esquema que seguiremos es el siguiente.
Primero, exploraremos diferentes opciones de persistencia de manera independiente, sin tener en cuenta las habilidades del proyecto anterior.
Después, actualizaremos las habilidades que ya hemos creado para incluir persistencia y facilitar su uso.
En tercer lugar, veremos otras formas de conseguir persistencia y formas de utilizarlas sin modificar el código de las habilidades.
Finalmente, crearemos habilidades nuevas que harán uso de la persistencia

## Actividades del proyecto

### 0. Descarga del proyecto

El primer paso para desarrollar el proyecto es descargar los ficheros necesarios del repositorio de Github.
El método más sencillo es a través del botón `Code->Download ZIP`.
Los ficheros necesarios para el proyecto son  `persistencia.py`, `estado_int.py`, `estado_pickle.py`, `estado_json.py` y `test.py`.
Además, también es necesario el fichero `habilidades.py` desarrollado en el proyecto anterior, por lo que deberá copiarse dentro de la carpeta del proyecto 4.

El primero es un fichero de plantilla que contiene la definición de varias funciones que son útiles para el proyecto (este será el fichero que se debe entregar en Moodle).
El fichero `estado_int.py` contiene código de ejemplo para la actividad 1.
Los ficheros `estado_pickle.py` y `estado_json.py` son plantillas que podemos usar para desarrollar y probar la segunda parte de la actividad 1 y la actividad 2.
Sin embargo, la solución final debe incorporarse en el fichero `persistencia.py`.
Para su edición, se puede usar cualquier IDE, aunque se recomienda Visual Studio Code. Para comprobar las soluciones, se proponen dos opciones. Por otro lado, el fichero `test.py`, se puede usar opcionalmente para comprobar que las funciones desarrolladas en el proyecto funcionan correctamente, como veremos más adelante.


### 1. Persistencia básica

La persistencia consiste guardar parte o la totalidad del estado de un programa, de forma que se pueda utilizar en ejecuciones posteriores.
En nuestro caso, guardaremos objetos con los que trabajamos (listas, diccionarios, etc.).

Existen infinidad de tipos de almacenamiento (en un fichero en nuestro disco, en una base de datos, en nuestro correo, etc.).
En este proyecto cubriremos varias opciones de almacenamiento, empezando por las más básicas.

Pero, antes de eso, debemos preguntarnos: ¿qué es exactamente lo que vamos a guardar?.
Los objetos en Python son, en el fondo, ceros y unos (bits, bytes) en la memoria RAM de nuestro sistema.
Para poder guardar un objeto en un fichero, necesitamos poder transformarlo a un formato que pueda escribirse y, sobre todo, que nos permita recuperar el objeto en el futuro.
El proceso de transformar objetos a un formato legible se conoce como **serialización**, y su inverso es la **deserialización**.

Dependiendo del tipo de objeto que tengamos, el proceso de serialización y deserialización puede variar.
Por ejemplo, imaginemos que nuestro programa sólo tiene como estado un contador, que queremos que se reutilice entre ejecuciones.
En ese caso, podrı́amos guardar nuestro contador (de tipo entero, `int`) en forma de cadena de texto en un fichero.
En ejecuciones posteriores podremos recuperar el valor del contador leyendo el fichero, y convirtiendo el texto al tipo que nos interesa (`int`), de forma similar a como hacíamos en el menú de proyectos anteriores.
El código podrı́a ser el siguiente:

<img src="./img/python.png" align=right width=100px>

```python
import os
FICHERO = 'estado.txt'

def leer_estado(fichero=FICHERO):
  if not os.path.exists(fichero):
    return 0

  with open(fichero, 'r') as f:
    return int(f.read())

def guardar_estado(estado, fichero=FICHERO):
  with open(fichero, 'w') as f:
    f.write(str(estado))

contador = leer_estado()
print(f'El contador vale {contador}')
contador += 1
guardar_estado(contador)
```

Si guardamos este código en un fichero (`estado_int.py`) y lo ejecutamos varias veces, vemos que el contador va aumentando:

<img src="./img/shell.png" align=right width=100px>

```shell
$ python estado_int.py
El contador vale 0
$ python estado_int.py
El contador vale 1
$ python estado_int.py
El contador vale 2
```

Podemos abrir manualmente el fichero `estado.txt` con un editor de texto y ver el valor del contador.
También podemos editar el valor.
Si cambiáramos en un editor el texto por `99`, si volvemos a ejecutar nuestro código veríamos lo siguiente:

<img src="./img/shell.png" align=right width=100px>

```shell
$ python estado_int.py
El contador vale 99
$ python estado_int.py
El contador vale 99
```

Sin embargo, esta función está limitada a guardar enteros, no permite guardar otro tipo de información tales como cadenas de texto, diccionarios, etc.

Para poder guardar y recuperar (casi) cualquier tipo de objeto en Python, existe un módulo en la biblioteca estándar de Python llamado `pickle`<sup>[1](#pickle)</sup>.
El módulo `pickle` implementa protocolos binarios para serializar y deserializar objetos Python.
Mediante la función `pickle.dump` de este módulo podremos hacer que un objeto Python se guarde en el fichero (en forma de cadena de bytes), y usando `pickle.load` conseguimos la operación inversa, es decir, leer el contenido de un fichero y generar un objeto Python.

__**Nota**: El argumento `pickle.dump` y `pickle.load` debe ser un fichero abierto en modo binario. En los ejemplos de código ya se proporciona esta parte.__

__**Nota**: El objeto guardado puede a su vez contener objetos dentro.
Por ejemplo, podríamos guardar un diccionario de diccionarios.__

Utilizando las funciones del módulo `pickle`, se pide modificar el código de las siguientes funciones, definidas en el fichero `solucion.py`, para que nos permita utilizar cualquier objeto Python:

<img src="./img/python.png" align=right width=100px>

```python
import pickle
import os

FICHERO_PICKLE = 'estado.pickle'

def leer_estado_pickle(fichero=FICHERO_PICKLE):
  if not os.path.exists(fichero):
    raise NotImplementedError

  with open(fichero, 'rb') as f:
    raise NotImplementedError

def guardar_estado_pickle(estado, fichero=FICHERO_PICKLE):
  with open(fichero, 'wb') as f:
    raise NotImplementedError

if __name__ == '__main__':
  estado = leer_estado_pickle()
  print(f'El estado vale {estado}')
  estado['contador'] = estado.get('contador', 0) + 1
  guardar_estado_pickle(estado)
```

Una vez implementado el código, el resultado de ejecutarlo las primeras veces deberı́a ser el siguiente:

<img src="./img/shell.png" align=right width=100px>

```shell
$ python estado_pickle.py
El estado es {}
$ python estado_pickle.py
El estado es {'contador': 1}
$ python estado_pickle.py
El estado es {'contador': 2}
$ python estado_pickle.py
El estado es {'contador': 3}
```

__**Nota**: Para probar el comportamiento de cero, o en caso de haber algún error de lectura/escritura del fichero, se puede borrar el fichero `estado.pickle` manualmente.__

__**Nota**: Pickle no está limitado a guardar tipos de datos simples como diccionarios o listas. También es capaz de guardar objetos complejos como un menú o una habilidad. La desventaja es que, una vez guardado un menú o una habilidad, se hace muy difı́cil actualizar su comportamiento (es decir, su código). No obstante, es una muy buena alternativa cuando se quiere guardar el estado muy rápidamente.__


### 2. Serialización en texto plano

El formato Pickle es muy potente ya que nos permite serializar casi cualquier objeto Python, pero tiene varias limitaciones. La principal es que es un formato binario especı́fico para Python: otros lenguajes de programación no pueden leerlo, y tampoco es legible por humanos. Como solución, vamos a implementar un formato de serialización que podremos escribir en fichero y que podremos leer tanto con un editor de texto como con cualquier otro lenguaje de programación.

Como desventaja, este enfoque sólo funciona para guardar los tipos de objeto más básicos: números, cadenas de texto, listas y diccionarios. El formato que usaremos es JSON (JavaScript Object Notation)<sup>[2](#json)</sup>, que fue originalmente diseñado para JavaScript pero dada su gran popularidad hoy en dı́a puede ser utilizado desde cualquier lenguaje. En Python podemos leer este formato utilizando el módulo `json`, de la biblioteca estándar. El módulo nos da funciones para leer y escribir tanto desde cadenas de texto como desde un fichero. El formato JSON es muy parecido a la notación en Python. Podemos ver un ejemplo de uso a continuación, en el que partimos de un diccionario, lo serializamos a formato JSON (`json.dumps`), y después lo
deserializamos de vuelta a Python (`json.loads`).

<img src="./img/python-repl-vertical.png" align=right width=100px>

```pycon
>>> import json
>>> datos = {'clave': 'valor', 'otraclave': [1,2,3]}
>>> serializado = json.dumps(datos)
>>> serializado
'{"clave": "valor", "otraclave": [1, 2, 3]}'
>>> deserializado = json.loads(serializado)
>>> deserializado
{'clave': 'valor', 'otraclave': [1, 2, 3]}
```

__**Nota**: El módulo `json` permite leer y escribir tanto de strings como de ficheros.
Para usar strings existen las funciones `json.loads` y `json.dumps`.
Desde ficheros usarı́amos `json.load` y `json.dump`, respectivamente.__

Se pide modificar el código a continuación para que permita guardar el estado del programa en un fichero JSON. El funcionamiento general del programa ha de ser idéntico al del apartado anterior.

<img src="./img/python.png" align=right width=100px>

```python
import json
import os

FICHERO_JSON = 'estado.json'

def leer_estado_json(fichero=FICHERO_JSON):
  if not os.path.exists(fichero):
    raise NotImplementedError

  with open(fichero, 'r') as f:
    raise NotImplementedError

def guardar_estado_json(estado, fichero=FICHERO_JSON):
  with open(fichero, 'w') as f:
    raise NotImplementedError

if __name__ == '__main__':
  estado = leer_estado_json()
  print(f'El estado vale {estado}')
  estado['contador'] = estado.get('contador', 0) + 1
  guardar_estado_json(estado)
```

Una vez lanzado el programa, deberı́a haberse creado el fichero `estado.json`. Pruebe a visualizarlo con un editor y a cambiar el valor del contador manualmente. En la próxima ejecución del programa este deberı́a utilizar el valor del contador introducido.


### 3. Clase Almacén
En este punto tenemos dos posibles implementaciones genéricas para persistencia: Pickle y JSON. Para añadir persistencia a nuestras habilidades, ¿cuál de las dos deberı́amos utilizar?. Y, ¿qué hacemos si en un futuro aparece algún otro tipo de persistencia (p.e., a una base de datos o a la nube)?.

En realidad, desde el punto de vista de nuestras habilidades, el tipo especı́fico de persistencia no influye para nada en el funcionamiento. Sólo necesitamos poder guardar y leer el estado. Por ello, en lugar de introducir directamente los métodos que hemos visto antes, vamos a crear una clase
nueva, a la que llamaremos Almacen. Esta clase incluirá un método para guardar estado y otro para leerlo.

A la hora de crear nuestras clases con persistencia, simplemente podremos proporcionarles una instancia de Almacen que se encargará de la persistencia. Esta clase se nos proporciona en la plantilla del ejercicio. También se proporcionan dos subclases. La
primera, EnMemoria es una clase de ejemplo que simplemente utiliza su estado interno para guardar el estado, sin ningún tipo de persistencia. La segunda, es una subclase que utilizaremos en almacenes que escriban en fichero, y veremos su utilidad más adelante. El código se puede ver a continuación:

<img src="./img/python.png" align=right width=100px>

```python
class Almacen:
  '''Clase genérica para los almacenes de estado'''

  def guardar(self, estado):
    '''Guarda el valor del estado.'''
    raise NotImplementedError

  def leer(self, defecto=None):
    '''
    Devuelve el valor guardado del estado.
    Si no hay un valor guardado, se devuelve defecto.
    '''
    raise NotImplementedError

class EnMemoria(Almacen):
  '''Guarda valores en memoria (sin persistencia en disco)'''
    
  def __init__(self):
    self.estado = {}
  
  def guardar(self, estado):
    self.estado = estado.copy()

  def leer(self, defecto=None):
    return self.estado or defecto

class AlmacenFichero(Almacen):
  '''Clase para heredar en los almacenes que persistan a fichero'''
  
  def __init__(self, fichero):
    self.fichero = fichero
```

Se pide implementar las dos siguientes clases, utilizando los métodos del primer apartado:

<img src="./img/python.png" align=right width=100px>

```python
class AlmacenPickle(AlmacenFichero):
  '''Guarda el estado en un Pickle '''
  
  def guardar(self, estado):
    raise NotImplementedError
  
  def leer(self, defecto=None):
    raise NotImplementedError
  
class AlmacenJSON(AlmacenFichero):
  '''Guarda el estado en un JSON'''
  
  def guardar(self, estado):
    raise NotImplementedError
  
  def leer(self, defecto={}):
    raise NotImplementedError
```

### 4. Habilidad lista de la compra con excepciones

En esta sección vamos a mejorar nuestra habilidad de `ListaDeLaCompra`, añadiendo excepciones.
Para ello, partiremos del código desarrollado en el proyecto 3, y modificaremos los métodos insertar y borrar para que incluyan excepciones.
Las excepciones a lanzar serán dos:

- En el método `insertar`, se deberá lanzar una excepción si el producto recibido como parámetro es nulo.

- En el método `borrar`, se deberá lanzar una excepción si el número de producto pasado no existe.

El código de partida, que también está disponible en la plantilla, es el siguiente:

<img src="./img/python.png" align=right width=100px>

```python
class ListaDeLaCompra(HabilidadSubcomandos):
  '''Gestión de lista de la compra que incluye excepciones'''

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.productos = []

  def subcomandos(self):
    return {
      'insertar': self.insertar,
      'borrar': self.borrar,
      'listar': self.listar,
      'cantidad': self.cantidad,
      }

  def insertar(self, producto):
    '''Insertar un producto nuevo, lanzando una excepción si el producto es nulo o contiene un string vacío'''
    raise NotImplementedError

  def listar(self):
    '''Mostrar el listado de productos'''
    for ix, producto in enumerate(self.productos):
      print(f'{ix}: {producto}')

  def borrar(self, numero):
    '''Borrar un producto, lanzando una excepción si el número de producto recibido no existe'''
    raise NotImplementedError

  def cantidad(self):
    '''Mostrar el número de productos en la lista'''
    return len(self.productos)
```

Se pide reemplazar las lı́neas marcadas con `raise NotImplementedError` con el código necesario para conseguir la funcionalidad.

### 5. Habilidad lista de la compra con persistencia

En esta sección vamos a mejorar nuestra habilidad de `ListaDeLaCompra`, añadiendo persistencia. En lugar de modificar el código directamente, lo que haremos será crear una subclase que herede de `ListaDeLaCompra` y que incluya la persistencia. El código necesario se proporciona a continuación. Los cambios necesarios serán:

- Añadir un parámetro almacen al constructor, que será usado para persistir el estado.

- Guardar el estado en el almacén cada vez que se hace una modificación de la lista de la compra.

El código de partida, que también está disponible en la plantilla, es el siguiente:

<img src="./img/python.png" align=right width=100px>

```python
class ListaDeLaCompraAlmacenada(ListaDeLaCompra):
  '''
  Habilidad igual en funcionamiento a ListaDeLaCompra, pero guardando
  la lista de productos en un almacén.
  '''

  def __init__(self, *args, almacen=EnMemoria, **kwargs):
    '''Recupera la lista de productos del almacén al crear el producto'''
    super().__init__(*args, **kwargs)
    raise NotImplementedError

  def insertar(self, producto):
    '''Guarda la nueva producto en el almacén además de añadirlo a la lista.'''
    super().insertar(producto)
    raise NotImplementedError

  def borrar(self, numero):
    '''Borra el producto del almacén además de borrarlo de la lista.'''
    super().borrar(numero)
    raise NotImplementedError
```

Se pide reemplazar las lı́neas marcadas con `raise NotImplementedError` con el código necesario para conseguir la funcionalidad.

### 6. Actividades opcionales

Para practicar tanto los conceptos de subclases como diferentes opciones de persistencia, se propone implementar las siguientes clases:

- `ListaContactos` una HabilidadSubcomandos que permite guardar contactos e información sobre ellos: números de teléfono, dirección, etc.

- `MultiAlmacen` un almacén que guarda los valores a varios almacenes internos. Sólo utiliza un almacén para la lectura: el primero de la lista de almacenes proporcionada.

- `AlmacenBackup` un almacen que recubre a otro almacén de la clase `AlmacenFichero` y guarda una copia del estado cada vez que se guarda.

- `AlmacenCSV` un almacén que guarda diccionarios en un fichero CSV<sup>[3](#csv)</sup>. El fichero CSV tendrá dos columnas, una para la clave del diccionario, y otra para el valor. Las claves serán siempre strings, pero el valor ha de ser serializado en formato JSON para escribirlo en el CSV. Al crear el almacen se le proporcionan los nombres de las columnas que puede tener el fichero CSV. 

- `AlmacenCSVAvanzado` (avanzado) un almacén que guarda estados en forma de diccionarios. Para cada clave del diccionario, debe existir una columna en el fichero CSV. Los ficheros resultantes sólo tendrán dos lı́neas: una con las cabeceras del CSV (los nombres de las columnas) y otra con los valores de cada columna.

- `AlmacenCSVBackup` (avanzado) igual que `AlmacenCSVAvanzado`, pero se guarda todo el historial de estados guardados. Cada vez que se guarda un estado, se añade una lı́nea al fichero CSV. Si alguna de las claves del estado nuevo no están entre las columnas, se ignoran pero se muestra un mensaje por pantalla con un aviso.

- `AlmacenCSVBackupAvanzado` (avanzado) igual que `AlmacenCSVBackup`, pero añadiendo las columnas necesarias al fichero cada vez que se introduce un estado nuevo en lugar de ignorar la clave. Nótese que, en caso de que haya que añadir alguna columna nueva, se deberá recrear todo el fichero para añadir la columna a los estados anteriores. El valor por defecto si no existı́a la clave en un estado anterior será `None`.

## Entrega del proyecto

Para entregar el proyecto, se deberá subir a Moodle en la tarea "Entrega del proyecto 4".
</br>
</br>

## Anexos
### Evaluación

El repositorio del proyecto contiene el fichero `test.py`.
Los tests pueden invocarse en cualquier momento en la lı́nea de comando. Si todo está bien implementado, deberı́a obtenerse un resultado parecido a este:

<img src="./img/shell.png" align=right width=100px>

```shell
$ python test.py
test_persistencia (__main__.TestPersistencia)
Comprobar que las funciones de leer y guardar funcionan
... no existe el fichero test.pickle
ok
test_persistencia_backup (__main__.TestPersistencia)
Deberı́a haber una copia cada vez que se guarda ... ok
test_tareas_enmemoria_compartido (__main__.TestPersistencia)
El almacenamiento en memoria se puede compartir ... ok
test_tareas_enmemoria_independiente (__main__.TestPersistencia)
El almacenamiento en memoria no da persistencia ... ok
test_tareas_json (__main__.TestPersistencia)
El almacenamiento en JSON da persistencia ... ok
test_tareas_multi (__main__.TestPersistencia) ... ok
----------------------------------------------------------------------
Ran 6 tests in 0.003s
OK
```

Si, por el contrario, hay algún fallo en el código, se mostrará el número de tests lanzados y el de fallos. Por ejemplo, al lanzarlo la primera vez sin haber hecho ningún apartado la salida deberı́a ser similar a esta:

<img src="./img/shell.png" align=right width=100px>

```shell
❯ python test.py | head -n 20
test_persistencia (__main__.TestPersistencia)
Comprobar que las funciones de leer y guardar funcionan ... ERROR
test_persistencia_backup (__main__.TestPersistencia)
Debería haber una copia cada vez que se guarda ... skipped 'AlmacenBackup no ha sido implementado'
test_productos_enmemoria_compartido (__main__.TestPersistencia)
El almacenamiento en memoria se puede compartir ... ERROR
test_productos_enmemoria_independiente (__main__.TestPersistencia)
El almacenamiento en memoria no da persistencia ... ERROR
test_productos_excepciones (__main__.TestPersistencia)
La lista de la compra lanza excepciones ... ERROR
test_productos_json (__main__.TestPersistencia)
El almacenamiento en JSON da persistencia ... ERROR
test_productos_multi (__main__.TestPersistencia) ... ERROR

======================================================================
ERROR: test_persistencia (__main__.TestPersistencia)
Comprobar que las funciones de leer y guardar funcionan
----------------------------------------------------------------------
Traceback (most recent call last):
  File "test.py", line 95, in test_persistencia
    assert not leer_estado_pickle()
  File "/proyecto4-persistencia/persistencia.py", line 16, in leer_estado_pickle
    raise NotImplementedError
NotImplementedError

[... SALIDA RECORTADA ...]

----------------------------------------------------------------------
Ran 7 tests in 0.002s

FAILED (errors=6, skipped=1)

```

### Convenciones

Durante el proyecto se utilizarán tres tipos de código. Por un lado, código a escribir en la línea de comandos
(_command line_), también conocida como terminal o consola. En el ejemplo de abajo, vemos cómo ejecutamos
el comando <img src="./img/python.png" align=right width=100px>

```python --version```, que imprime por pantalla la versión de Python en el sistema.

<img src="./img/shell.png" align=right width=100px>

```shell
$ python --version
Python 3.10.12
```

Por otro lado, hay fragmentos de sesión del intérprete de comandos de python.
Podemos acceder al intérprete directamente ejecutando el comando Python en nuestra terminal:

<img src="./img/shell.png" align=right width=100px>

```shell
$ python
Python 3.10.12 (main, Jun 11 2023, 05:26:28) [GCC 11.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> 
```

En este punto, podemos empezar a introducir nuestro código Python.
Las líneas introducidas por el usuario son las que empiezan con "```>>>```" o "```...```", como en el ejemplo siguiente:

<img src="./img/python-repl-vertical.png" align=right width=100px>

```pycon
Esto es código python
>>> a = 2
>>> for i in range(a):
...     print(i)
...
0
1
```

Finalmente, habrá código de ejemplo a guardar en un fichero de texto:

<img src="./img/python.png" align=right width=100px>

```python
def funcion(parametro):
   return
```

También utilizaremos notas para resaltar consejos o aspectos importantes:

_**Nota**: todas las líneas ejecutadas durante una sesión de python o de consola se guardan en el historial. Se puede acceder a una línea anterior mediante las flechas del teclado o pulsando ```Ctrl+P``` repetidamente hasta llegar a la línea deseada._

## Enlaces
<a name="pickle">1</a>: https://docs.python.org/3/library/pickle.html</br>
<a name="json">2</a>: https://www.json.org </br>
<a name="csv">3</a>: https://docs.python.org/3/library/csv.html </br>
