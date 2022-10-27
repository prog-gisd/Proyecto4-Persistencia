import pickle
import os
import csv
import json
import shutil

from datetime import datetime

from habilidades import HabilidadCompleja

FICHERO_PICKLE = 'estado.pickle'
FICHERO_JSON = 'estado.json'

def leer_estado_pickle(fichero=FICHERO_PICKLE):
    if not os.path.exists(fichero):
        raise NotImplementedError

    with open(fichero, 'rb') as f:
        raise NotImplementedError

def guardar_estado_pickle(estado, fichero=FICHERO_PICKLE):
    with open(fichero, 'wb') as f:
        raise NotImplementedError

def leer_estado_json(fichero=FICHERO_JSON):
    '''Recupera el estado desde un JSON'''
    if not os.path.exists(fichero):
        raise NotImplementedError

    with open(fichero, 'r', encoding='utf8') as f:
        raise NotImplementedError
    return {}

def guardar_estado_json(estado, fichero=FICHERO_JSON):
    '''Guarda el estado proporcionado en un JSON'''
    with open(fichero, 'w', encoding='utf8') as f:
        raise NotImplementedError

class Almacen:
    '''Clase genérica para los almacenes de estado'''

    def guardar(self, estado):
        '''Guarda el valor del estado.'''
        raise NotImplementedError

    def leer(self, defecto=None):
        '''Devuelve el valor guardado del estado'''
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
    '''Clase para heredar en los almacenes que usen un fichero'''
    def __init__(self, fichero):
        raise NotImplementedError

class AlmacenPickle(Almacen):
    def __init__(self, fichero):
        raise NotImplementedError

    def guardar(self, estado):
        raise NotImplementedError

    def leer(self, defecto=None):
        raise NotImplementedError


class AlmacenJSON(Almacen):

    def __init__(self, fichero):
        raise NotImplementedError

    def guardar(self, estado):
        raise NotImplementedError

    def leer(self, defecto={}):
        raise NotImplementedError


class MultiAlmacen(Almacen):
    def __init__(self, almacenes):
        raise NotImplementedError

    def guardar(self, estado):
        raise NotImplementedError

    def leer(self, *args, **kwargs):
        raise NotImplementedError

class ListaDeLaCompra(HabilidadCompleja):
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

class ListaDeLaCompraAlmacenada(ListaDeLaCompra):

    def __init__(self, *args, almacen=EnMemoria, **kwargs):
        super().__init__(*args, **kwargs)
        raise NotImplementedError

    def insertar(self, producto):
        super().insertar(producto)
        raise NotImplementedError

    def borrar(self, numero):
        super().borrar(numero)
        raise NotImplementedError
