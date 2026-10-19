from dataclasses import dataclass
from datetime import datetime

from dominio.reglas import ACTIVIDADES


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


def validar_seleccion(actividad, horario):
    if not actividad:
        raise ErrorInscripcion("Debe seleccionar una actividad")
    if actividad not in ACTIVIDADES:
        raise ErrorInscripcion("La actividad seleccionada no existe")
    if not horario:
        raise ErrorInscripcion("Debe seleccionar un horario")


def validar_visitante(visitante):
    if not visitante.nombre:
        raise ErrorInscripcion("Debe ingresar el nombre de cada visitante")
    if not visitante.dni:
        raise ErrorInscripcion("Debe ingresar el DNI de cada visitante")
    if not visitante.dni.isdigit() or len(visitante.dni) not in (7, 8):
        raise ErrorInscripcion(
            "El DNI debe tener 7 u 8 dígitos, sin puntos ni espacios")
    if not visitante.edad:
        raise ErrorInscripcion("Debe ingresar la edad de cada visitante")


def inscribir(actividad, horario, cantidad, visitantes, acepta_terminos,
              registro):
    validar_seleccion(actividad, horario)
    for visitante in visitantes:
        validar_visitante(visitante)
    if not acepta_terminos:
        raise ErrorInscripcion(
            "Debe aceptar los términos y condiciones de la actividad")
    inscripcion = Inscripcion(actividad, horario, visitantes)
    registro.append(inscripcion)
