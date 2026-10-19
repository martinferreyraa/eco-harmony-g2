from dataclasses import dataclass
from datetime import datetime


class ErrorInscripcion(Exception):
    pass


@dataclass
class Visitante:
    nombre: str
    dni: str
    edad: str


@dataclass
class Inscripcion:
    actividad: str
    horario: datetime
    visitantes: list


def inscribir(actividad, horario, cantidad, visitantes, acepta_terminos,
              registro):
    if not actividad:
        raise ErrorInscripcion("Debe seleccionar una actividad")
    if not horario:
        raise ErrorInscripcion("Debe seleccionar un horario")
    for visitante in visitantes:
        if not visitante.nombre:
            raise ErrorInscripcion(
                "Debe ingresar el nombre de cada visitante")
        if not visitante.dni:
            raise ErrorInscripcion("Debe ingresar el DNI de cada visitante")
        if not visitante.edad:
            raise ErrorInscripcion(
                "Debe ingresar la edad de cada visitante")
    inscripcion = Inscripcion(actividad, horario, visitantes)
    registro.append(inscripcion)
