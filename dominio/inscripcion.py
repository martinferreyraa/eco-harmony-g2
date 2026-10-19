from dataclasses import dataclass
from datetime import datetime

from dominio.reglas import (ACTIVIDADES, ANTICIPACION_MAXIMA,
                            ANTICIPACION_MINIMA, CUPOS,
                            EDAD_MINIMA, FERIADOS, HORA_PRIMER_TURNO,
                            HORA_ULTIMO_TURNO, LUNES, REQUIEREN_TALLE,
                            TALLES)


class ErrorInscripcion(Exception):
    pass


@dataclass
class Visitante:
    nombre: str
    dni: str
    edad: str
    talle: str = ""


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
    if not visitante.edad.isdigit() or int(visitante.edad) > 120:
        raise ErrorInscripcion(
            "La edad debe ser un número entero entre 0 y 120")


def validar_reglas_de_actividad(visitante, actividad):
    if actividad in REQUIEREN_TALLE:
        if not visitante.talle:
            raise ErrorInscripcion(
                f"{actividad} requiere el talle de cada visitante")
        if visitante.talle not in TALLES:
            raise ErrorInscripcion(
                "El talle debe ser uno de: " + ", ".join(TALLES))
    edad_minima = EDAD_MINIMA.get(actividad, 0)
    if int(visitante.edad) < edad_minima:
        raise ErrorInscripcion(
            f"La edad mínima para {actividad} es {edad_minima} años")


def validar_cantidad(cantidad, visitantes):
    if cantidad < 1:
        raise ErrorInscripcion("Debe indicar al menos una persona")
    if cantidad != len(visitantes):
        raise ErrorInscripcion(
            "La cantidad de personas no coincide con los visitantes "
            "ingresados")


def cupo_disponible(actividad, horario, registro):
    ocupados = 0
    for anterior in registro:
        if anterior.actividad == actividad and anterior.horario == horario:
            ocupados += len(anterior.visitantes)
    return CUPOS[actividad] - ocupados


def validar_cupo(actividad, horario, cantidad, registro):
    disponibles = cupo_disponible(actividad, horario, registro)
    if disponibles <= 0:
        raise ErrorInscripcion(
            f"No hay cupo disponible para {actividad} en ese horario")
    if cantidad > disponibles:
        raise ErrorInscripcion(
            f"Solo quedan {disponibles} lugares disponibles para "
            f"{actividad} en ese horario")


def validar_turno(horario):
    es_turno_en_punto = horario.minute == 0
    esta_en_rango = HORA_PRIMER_TURNO <= horario.hour <= HORA_ULTIMO_TURNO
    if not es_turno_en_punto or not esta_en_rango:
        raise ErrorInscripcion(
            "El horario debe ser un turno en punto entre las "
            f"{HORA_PRIMER_TURNO} y las {HORA_ULTIMO_TURNO} hs")
    if horario.weekday() == LUNES:
        raise ErrorInscripcion("El parque está cerrado los lunes")
    if (horario.day, horario.month) in FERIADOS:
        raise ErrorInscripcion("El parque está cerrado el 25/12 y el 1/1")


def validar_anticipacion(horario, ahora):
    if horario < ahora:
        raise ErrorInscripcion("El turno seleccionado ya pasó")
    if horario - ahora > ANTICIPACION_MAXIMA:
        raise ErrorInscripcion(
            "Solo se puede reservar desde 24 hs antes del turno")
    if horario - ahora < ANTICIPACION_MINIMA:
        raise ErrorInscripcion(
            "Se debe reservar al menos 15 minutos antes del turno")


def dnis_inscriptos(horario, registro):
    dnis = []
    for anterior in registro:
        if anterior.horario == horario:
            for inscripto in anterior.visitantes:
                dnis.append(inscripto.dni)
    return dnis


def validar_superposicion(horario, visitantes, registro):
    ya_inscriptos = dnis_inscriptos(horario, registro)
    for visitante in visitantes:
        if visitante.dni in ya_inscriptos:
            raise ErrorInscripcion(
                f"El DNI {visitante.dni} ya tiene una inscripción en ese "
                "horario")


def inscribir(actividad, horario, cantidad, visitantes, acepta_terminos,
              registro, ahora, enviador):
    validar_seleccion(actividad, horario)
    validar_turno(horario)
    validar_anticipacion(horario, ahora)
    validar_cantidad(cantidad, visitantes)
    for visitante in visitantes:
        validar_visitante(visitante)
        validar_reglas_de_actividad(visitante, actividad)
    if not acepta_terminos:
        raise ErrorInscripcion(
            "Debe aceptar los términos y condiciones de la actividad")
    validar_cupo(actividad, horario, cantidad, registro)
    validar_superposicion(horario, visitantes, registro)
    inscripcion = Inscripcion(actividad, horario, visitantes)
    registro.append(inscripcion)
