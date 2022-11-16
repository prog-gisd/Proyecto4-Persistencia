import json
import os

FICHERO_JSON = "estado.json"


def leer_estado_json(fichero=FICHERO_JSON):
    if not os.path.exists(fichero):
        raise NotImplementedError

    with open(fichero, "r") as f:
        raise NotImplementedError


def guardar_estado_json(estado, fichero=FICHERO_JSON):
    with open(fichero, "w") as f:
        raise NotImplementedError


if __name__ == "__main__":
    estado = leer_estado_json()
    print(f"El estado vale {estado}")
    estado["contador"] = estado.get("contador", 0) + 1
    guardar_estado_json(estado)
