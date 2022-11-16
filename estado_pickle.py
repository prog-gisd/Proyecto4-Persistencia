import os
import pickle


FICHERO = "estado.pickle"


def leer_estado_pickle(fichero=FICHERO):
    if not os.path.exists(fichero):
        raise NotImplementedError

    with open(fichero, "rb") as f:
        raise NotImplementedError


def guardar_estado_pickle(estado, fichero=FICHERO):
    with open(fichero, "wb") as f:
        raise NotImplementedError


if __name__ == "__main__":
    estado = leer_estado_pickle()
    print(f"El estado vale {estado}")
    estado["contador"] = estado.get("contador", 0) + 1
    guardar_estado_pickle(estado)
