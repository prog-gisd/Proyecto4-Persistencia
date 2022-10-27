import os

FICHERO = 'estado.txt'

def leer_estado(fichero=FICHERO):
    if not os.path.exists(fichero):
        return 0

    with open(fichero, 'r') as f:
        return int(f.read())

def guardar_estado(estado, fichero=FICHERO):
    with open(fichero, 'w') as f:
        # Usar el protocolo más alto posible en esta versión
        f.write(str(estado))

contador = leer_estado()
print(f'El contador vale {contador}')
contador += 1
guardar_estado(contador)

