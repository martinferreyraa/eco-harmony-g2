from datetime import timedelta

from dominio.inscripcion import (ErrorInscripcion, Inscripcion, Visitante,
                                 validar_anticipacion, validar_turno)
from dominio.reglas import ANTICIPACION_MAXIMA, CUPOS


def es_reservable(turno, ahora):
    try:
        validar_turno(turno)
        validar_anticipacion(turno, ahora)
    except ErrorInscripcion:
        return False
    return True


def proximo_turno_reservable(ahora):
    # Prueba hora por hora, sin pasarse de la ventana de 24 hs
    turno = ahora.replace(minute=0, second=0, microsecond=0)
    while turno - ahora <= ANTICIPACION_MAXIMA:
        if es_reservable(turno, ahora):
            return turno
        turno += timedelta(hours=1)
    return None


def crear_seed(ahora):
    """Registro inicial de la demo: el próximo turno de Safari, lleno."""
    registro = []
    turno = proximo_turno_reservable(ahora)
    if turno is None:
        return registro
    visitantes = []
    for numero in range(CUPOS["Safari"]):
        dni = str(10000000 + numero)
        visitantes.append(Visitante(f"Visitante {numero + 1}", dni, "30"))
    registro.append(Inscripcion("Safari", turno, visitantes))
    return registro
