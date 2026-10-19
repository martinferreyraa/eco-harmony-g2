from dataclasses import dataclass
from datetime import datetime

from dominio.reglas import (ACTIVIDADES, ANTICIPACION_MAXIMA,
                            ANTICIPACION_MINIMA, CUPOS,
                            EDAD_MINIMA, FERIADOS, HORA_PRIMER_TURNO,
                            HORA_ULTIMO_TURNO, LUNES, REQUIEREN_TALLE,
                            TALLES)


FORMATO_FECHA_HORA = "%d/%m/%Y %H:%M"


class ErrorInscripcion(Exception):
    """Error con su mensaje y el campo del formulario donde mostrarlo."""

    def __init__(self, mensaje, campo=None):
        super().__init__(mensaje)
        self.campo = campo


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


@dataclass
class Mail:
    asunto: str
    cuerpo: str
    qrs: list


def validar_actividad(actividad):
    if not actividad:
        raise ErrorInscripcion("Debe seleccionar una actividad", "actividad")
    if actividad not in ACTIVIDADES:
        raise ErrorInscripcion("La actividad seleccionada no existe",
                               "actividad")


def validar_seleccion(actividad, horario):
    validar_actividad(actividad)
    if not horario:
        raise ErrorInscripcion("Debe seleccionar un horario", "horario")


def es_numero(texto):
    # isdigit() solo acepta también "²" o "٣"; isascii() deja solo 0 a 9
    return texto.isascii() and texto.isdigit()


def es_dni_valido(dni):
    # 7 u 8 dígitos sin ceros adelante: de 1.000.000 a 99.999.999
    if not es_numero(dni) or dni.startswith("0"):
        return False
    return len(dni) in (7, 8)


def es_palabra_de_nombre(palabra):
    # Empieza y termina con letra; adentro puede tener apóstrofo o guion
    if not palabra[0].isalpha() or not palabra[-1].isalpha():
        return False
    letras = 0
    for caracter in palabra:
        if caracter.isalpha():
            letras += 1
        elif caracter not in "'-":
            return False
    return letras >= 2


def es_nombre_completo(nombre):
    palabras = nombre.split()
    if len(palabras) < 2:
        return False
    for palabra in palabras:
        if not es_palabra_de_nombre(palabra):
            return False
    return True


def validar_visitante(visitante, indice):
    # indice: posición del visitante en el formulario (0 es el primero)
    if not visitante.nombre:
        raise ErrorInscripcion("Debe ingresar el nombre de cada visitante",
                               f"nombre-{indice}")
    if not es_nombre_completo(visitante.nombre):
        raise ErrorInscripcion(
            "Ingresá el nombre completo (nombre y apellido), solo con letras",
            f"nombre-{indice}")
    if not visitante.dni:
        raise ErrorInscripcion("Debe ingresar el DNI de cada visitante",
                               f"dni-{indice}")
    if not es_dni_valido(visitante.dni):
        raise ErrorInscripcion(
            "El DNI debe tener 7 u 8 dígitos, sin puntos, espacios ni "
            "ceros adelante", f"dni-{indice}")
    if not visitante.edad:
        raise ErrorInscripcion("Debe ingresar la edad de cada visitante",
                               f"edad-{indice}")
    if not es_numero(visitante.edad) or int(visitante.edad) > 120:
        raise ErrorInscripcion(
            "La edad debe ser un número entero entre 0 y 120",
            f"edad-{indice}")


def validar_reglas_de_actividad(visitante, actividad, indice):
    if actividad in REQUIEREN_TALLE:
        if not visitante.talle:
            raise ErrorInscripcion(
                f"{actividad} requiere el talle de cada visitante",
                f"talle-{indice}")
        if visitante.talle not in TALLES:
            raise ErrorInscripcion(
                "El talle debe ser uno de: " + ", ".join(TALLES),
                f"talle-{indice}")
    edad_minima = EDAD_MINIMA.get(actividad, 0)
    if int(visitante.edad) < edad_minima:
        raise ErrorInscripcion(
            f"La edad mínima para {actividad} es {edad_minima} años",
            f"edad-{indice}")


def es_reservable(turno, ahora):
    """True si el turno existe, el parque abre y está en la ventana."""
    try:
        validar_turno(turno)
        validar_anticipacion(turno, ahora)
    except ErrorInscripcion:
        return False
    return True


def validar_cantidad(cantidad, visitantes):
    if cantidad != len(visitantes):
        raise ErrorInscripcion(
            "La cantidad de personas no coincide con los visitantes "
            "ingresados", "cantidad")


def validar_dnis_distintos(visitantes):
    vistos = []
    for indice, visitante in enumerate(visitantes):
        if visitante.dni in vistos:
            raise ErrorInscripcion(
                f"El DNI {visitante.dni} está repetido en la inscripción",
                f"dni-{indice}")
        vistos.append(visitante.dni)


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
            f"No hay cupo disponible para {actividad} en ese horario",
            "horario")
    if cantidad > disponibles:
        raise ErrorInscripcion(
            f"Solo quedan {disponibles} lugares disponibles para "
            f"{actividad} en ese horario", "cantidad")


def validar_turno(horario):
    es_turno_en_punto = horario.minute == 0
    esta_en_rango = HORA_PRIMER_TURNO <= horario.hour <= HORA_ULTIMO_TURNO
    if not es_turno_en_punto or not esta_en_rango:
        raise ErrorInscripcion(
            "El horario debe ser un turno en punto entre las "
            f"{HORA_PRIMER_TURNO} y las {HORA_ULTIMO_TURNO} hs",
            "horario")
    if horario.weekday() == LUNES:
        raise ErrorInscripcion("El parque está cerrado los lunes",
                               "horario")
    if (horario.day, horario.month) in FERIADOS:
        raise ErrorInscripcion("El parque está cerrado el 25/12 y el 1/1",
                               "horario")


def validar_anticipacion(horario, ahora):
    if horario < ahora:
        raise ErrorInscripcion("El turno seleccionado ya pasó", "horario")
    if horario - ahora > ANTICIPACION_MAXIMA:
        raise ErrorInscripcion(
            "Solo se puede reservar desde 24 hs antes del turno",
            "horario")
    if horario - ahora < ANTICIPACION_MINIMA:
        raise ErrorInscripcion(
            "Se debe reservar al menos 15 minutos antes del turno",
            "horario")


def dnis_inscriptos(horario, registro):
    dnis = []
    for anterior in registro:
        if anterior.horario == horario:
            for inscripto in anterior.visitantes:
                dnis.append(inscripto.dni)
    return dnis


def validar_superposicion(horario, visitantes, registro):
    ya_inscriptos = dnis_inscriptos(horario, registro)
    for indice, visitante in enumerate(visitantes):
        if visitante.dni in ya_inscriptos:
            raise ErrorInscripcion(
                f"El DNI {visitante.dni} ya tiene una inscripción en ese "
                "horario", f"dni-{indice}")


def armar_cuerpo(numero_orden, actividad, horario, visitantes):
    lineas = [
        "Tu inscripción fue confirmada.",
        f"Número de orden: {numero_orden}",
        f"Actividad: {actividad}",
        "Fecha y hora: " + horario.strftime(FORMATO_FECHA_HORA),
        f"Cantidad de personas: {len(visitantes)}",
        "Visitantes:",
    ]
    for visitante in visitantes:
        linea = (f"- {visitante.nombre}, DNI {visitante.dni}, "
                 f"{visitante.edad} años")
        if visitante.talle:
            linea += f", talle {visitante.talle}"
        lineas.append(linea)
    return "\n".join(lineas)


def texto_qr(numero_orden, visitante, actividad, horario):
    fecha_hora = horario.strftime(FORMATO_FECHA_HORA)
    return (f"Orden {numero_orden} | {visitante.nombre} | "
            f"DNI {visitante.dni} | {actividad} | {fecha_hora}")


def armar_mail(numero_orden, actividad, horario, visitantes):
    cuerpo = armar_cuerpo(numero_orden, actividad, horario, visitantes)
    qrs = []
    for visitante in visitantes:
        qrs.append(texto_qr(numero_orden, visitante, actividad, horario))
    return Mail(f"Inscripción confirmada: {actividad}", cuerpo, qrs)


def validar_reserva(actividad, horario, cantidad, registro, ahora):
    """Lo que se elige en la primera pantalla: actividad, turno y cantidad.

    La web la usa al tocar Continuar; inscribir la vuelve a llamar al
    confirmar, por si el cupo se llenó mientras se cargaban los datos.
    """
    validar_seleccion(actividad, horario)
    validar_turno(horario)
    validar_anticipacion(horario, ahora)
    if cantidad < 1:
        raise ErrorInscripcion("Debe indicar al menos una persona",
                               "cantidad")
    validar_cupo(actividad, horario, cantidad, registro)


def inscribir(actividad, horario, cantidad, visitantes, acepta_terminos,
              registro, ahora, enviador):
    validar_reserva(actividad, horario, cantidad, registro, ahora)
    validar_cantidad(cantidad, visitantes)
    for indice, visitante in enumerate(visitantes):
        validar_visitante(visitante, indice)
        validar_reglas_de_actividad(visitante, actividad, indice)
    validar_dnis_distintos(visitantes)
    if not acepta_terminos:
        raise ErrorInscripcion(
            "Debe aceptar los términos y condiciones de la actividad",
            "terminos")
    validar_superposicion(horario, visitantes, registro)
    numero_orden = len(registro) + 1
    mail = armar_mail(numero_orden, actividad, horario, visitantes)
    try:
        enviador.enviar(mail)
    except OSError:
        # Errores de red y de SMTP: smtplib.SMTPException hereda de OSError
        raise ErrorInscripcion(
            "No se pudo enviar el mail de confirmación; "
            "la inscripción no se realizó")
    inscripcion = Inscripcion(actividad, horario, visitantes)
    registro.append(inscripcion)
