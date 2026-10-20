from datetime import datetime, timedelta
from pathlib import Path

from flask import Flask, render_template, request
from werkzeug.datastructures import MultiDict

from dominio.inscripcion import (ErrorInscripcion, Visitante, cupo_disponible,
                                 es_numero, es_reservable, inscribir,
                                 validar_reserva)
from dominio.reglas import (ACTIVIDADES, FERIADOS, HORA_PRIMER_TURNO,
                            HORA_ULTIMO_TURNO, LUNES, REQUIEREN_TALLE,
                            TALLES, TERMINOS)
from dominio.seed import crear_seed
from servicios.mail import EnviadorSMTP
from servicios.registro_sqlite import RegistroSQLite

app = Flask(__name__)

HORAS = list(range(HORA_PRIMER_TURNO, HORA_ULTIMO_TURNO + 1))
DIAS_CERRADOS = {"lunes": LUNES, "feriados": FERIADOS}
# Errores que se corrigen en la primera pantalla
CAMPOS_DE_LA_RESERVA = ["actividad", "horario", "cantidad"]
# En la raíz del proyecto, sin importar desde dónde se corre Flask
RUTA_BASE_DE_DATOS = Path(__file__).parent.parent / "eco_harmony.db"


def crear_registro():
    """Único lugar donde se crea el registro: la base SQLite y su seed."""
    registro = RegistroSQLite(RUTA_BASE_DE_DATOS)
    crear_seed(registro, datetime.now())
    return registro


registro = crear_registro()
enviador = EnviadorSMTP()


# --- Conversión de los datos del formulario (no valida: eso es del dominio)

def a_entero(texto):
    if es_numero(texto):
        return int(texto)
    return 0


def armar_horario(fecha, hora):
    try:
        return datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H")
    except ValueError:
        return None


def leer_reserva(datos):
    """Los cuatro datos de la primera pantalla, tal como llegan."""
    return {
        "actividad": datos.get("actividad", ""),
        "fecha": datos.get("fecha", ""),
        "hora": datos.get("hora", ""),
        "cantidad": datos.get("cantidad", ""),
    }


def armar_visitantes(formulario):
    visitantes = []
    datos = zip(formulario.getlist("nombre"), formulario.getlist("dni"),
                formulario.getlist("edad"), formulario.getlist("talle"))
    for nombre, dni, edad, talle in datos:
        visitantes.append(Visitante(nombre, dni, edad, talle))
    return visitantes


# --- Pantallas

def mostrar_inicio(reserva, error=None):
    hoy = datetime.now().date()
    return render_template(
        "inicio.html", actividades=ACTIVIDADES, horas=HORAS,
        dias_cerrados=DIAS_CERRADOS,
        fecha_minima=hoy.isoformat(),
        fecha_maxima=(hoy + timedelta(days=1)).isoformat(),
        reserva=reserva, error=error)


def mostrar_formulario(reserva, valores, error=None):
    actividad = reserva["actividad"]
    return render_template(
        "formulario.html", reserva=reserva,
        horario=armar_horario(reserva["fecha"], reserva["hora"]),
        cantidad=a_entero(reserva["cantidad"]), talles=TALLES,
        requiere_talle=actividad in REQUIEREN_TALLE,
        terminos=TERMINOS.get(actividad, ""), valores=valores, error=error)


# --- Rutas

@app.get("/")
def inicio():
    # Si viene del link "cambiar turno o cantidad", trae los valores cargados
    return mostrar_inicio(leer_reserva(request.args))


@app.get("/inscripcion")
def formulario():
    reserva = leer_reserva(request.args)
    horario = armar_horario(reserva["fecha"], reserva["hora"])
    try:
        validar_reserva(reserva["actividad"], horario,
                        a_entero(reserva["cantidad"]), registro,
                        datetime.now())
    except ErrorInscripcion as error:
        return mostrar_inicio(reserva, error)
    return mostrar_formulario(reserva, MultiDict())


@app.post("/inscripcion")
def confirmar():
    reserva = leer_reserva(request.form)
    horario = armar_horario(reserva["fecha"], reserva["hora"])
    visitantes = armar_visitantes(request.form)
    acepta_terminos = request.form.get("acepta_terminos") == "si"
    try:
        inscribir(reserva["actividad"], horario,
                  a_entero(reserva["cantidad"]), visitantes, acepta_terminos,
                  registro, datetime.now(), enviador)
    except ErrorInscripcion as error:
        if error.campo in CAMPOS_DE_LA_RESERVA:
            return mostrar_inicio(reserva, error)
        return mostrar_formulario(reserva, request.form, error)
    return render_template("confirmacion.html",
                           actividad=reserva["actividad"], horario=horario,
                           visitantes=visitantes)


@app.get("/cupos")
def cupos():
    ahora = datetime.now()
    fecha = request.args.get("fecha") or ahora.date().isoformat()
    if armar_horario(fecha, HORA_PRIMER_TURNO) is None:
        fecha = ahora.date().isoformat()
    filas = []
    for hora in HORAS:
        horario = armar_horario(fecha, hora)
        lugares = []
        for actividad in ACTIVIDADES:
            if es_reservable(horario, ahora):
                lugares.append(cupo_disponible(actividad, horario, registro))
            else:
                lugares.append(None)
        filas.append({"hora": f"{hora:02d}:00", "lugares": lugares})
    return render_template("cupos.html", fecha=fecha, filas=filas,
                           actividades=ACTIVIDADES,
                           dias_cerrados=DIAS_CERRADOS)
