from datetime import datetime, timedelta

from flask import Flask, render_template, request
from werkzeug.datastructures import MultiDict

from dominio.inscripcion import (ErrorInscripcion, Visitante, cupo_disponible,
                                 es_numero, es_reservable, inscribir)
from dominio.reglas import (ACTIVIDADES, CUPOS, FERIADOS, HORA_PRIMER_TURNO,
                            HORA_ULTIMO_TURNO, LUNES, REQUIEREN_TALLE,
                            TALLES, TERMINOS)
from dominio.seed import crear_seed
from servicios.mail import EnviadorSMTP

app = Flask(__name__)

HORAS = list(range(HORA_PRIMER_TURNO, HORA_ULTIMO_TURNO + 1))
MAXIMO_PERSONAS = max(CUPOS.values())
DIAS_CERRADOS = {"lunes": LUNES, "feriados": FERIADOS}


def crear_registro():
    """Único lugar donde se crea el registro (por ahora, en memoria)."""
    return crear_seed(datetime.now())


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


def armar_visitantes(formulario):
    visitantes = []
    datos = zip(formulario.getlist("nombre"), formulario.getlist("dni"),
                formulario.getlist("edad"), formulario.getlist("talle"))
    for nombre, dni, edad, talle in datos:
        visitantes.append(Visitante(nombre, dni, edad, talle))
    return visitantes


def mostrar_formulario(actividad, cantidad, valores, error=None):
    hoy = datetime.now().date()
    return render_template(
        "formulario.html", actividad=actividad, cantidad=cantidad,
        horas=HORAS, talles=TALLES,
        requiere_talle=actividad in REQUIEREN_TALLE,
        terminos=TERMINOS.get(actividad, ""),
        dias_cerrados=DIAS_CERRADOS, fecha_minima=hoy.isoformat(),
        fecha_maxima=(hoy + timedelta(days=1)).isoformat(),
        valores=valores, error=error)


# --- Rutas

@app.get("/")
def inicio():
    return render_template("inicio.html", actividades=ACTIVIDADES,
                           maximo_personas=MAXIMO_PERSONAS)


@app.get("/inscripcion")
def formulario():
    actividad = request.args.get("actividad", "")
    cantidad = a_entero(request.args.get("cantidad", ""))
    return mostrar_formulario(actividad, cantidad, MultiDict())


@app.post("/inscripcion")
def confirmar():
    actividad = request.form.get("actividad", "")
    cantidad = a_entero(request.form.get("cantidad", ""))
    horario = armar_horario(request.form.get("fecha", ""),
                            request.form.get("hora", ""))
    visitantes = armar_visitantes(request.form)
    acepta_terminos = request.form.get("acepta_terminos") == "si"
    try:
        inscribir(actividad, horario, cantidad, visitantes, acepta_terminos,
                  registro, datetime.now(), enviador)
    except ErrorInscripcion as error:
        return mostrar_formulario(actividad, cantidad, request.form,
                                  str(error))
    return render_template("confirmacion.html", actividad=actividad,
                           horario=horario, visitantes=visitantes)


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
