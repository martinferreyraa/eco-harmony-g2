from datetime import timedelta

from dominio.inscripcion import Inscripcion, Visitante, es_reservable
from dominio.reglas import ANTICIPACION_MAXIMA, CUPOS


def proximo_turno_reservable(ahora):
    # Prueba hora por hora, sin pasarse de la ventana de 24 hs
    turno = ahora.replace(minute=0, second=0, microsecond=0)
    while turno - ahora <= ANTICIPACION_MAXIMA:
        if es_reservable(turno, ahora):
            return turno
        turno += timedelta(hours=1)
    return None


def crear_seed(registro, ahora):
    """Datos de la demo: llena el próximo turno de Safari en el registro."""
    turno = proximo_turno_reservable(ahora)
    if turno is None:
        return
    visitantes = []
    for numero in range(CUPOS["Safari"]):
        dni = str(10000000 + numero)
        visitantes.append(Visitante(f"Visitante {numero + 1}", dni, "30"))
    registro.append(Inscripcion("Safari", turno, visitantes))
