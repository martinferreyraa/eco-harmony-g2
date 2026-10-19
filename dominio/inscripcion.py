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
    inscripcion = Inscripcion(actividad, horario, visitantes)
    registro.append(inscripcion)
