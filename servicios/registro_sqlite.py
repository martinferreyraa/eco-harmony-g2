import sqlite3
from datetime import datetime

from dominio.inscripcion import Inscripcion, Visitante

CREAR_TABLAS = """
CREATE TABLE IF NOT EXISTS inscripciones (
    id INTEGER PRIMARY KEY,
    actividad TEXT,
    horario TEXT
);
CREATE TABLE IF NOT EXISTS visitantes (
    id INTEGER PRIMARY KEY,
    inscripcion_id INTEGER REFERENCES inscripciones(id),
    nombre TEXT,
    dni TEXT,
    edad TEXT,
    talle TEXT
);
"""


class RegistroSQLite:
    """Reemplaza a la lista de inscripciones: append, recorrer y contar.

    Abre una conexión por operación porque Flask atiende con hilos y una
    conexión de sqlite3 no se comparte entre hilos.
    """

    def __init__(self, ruta):
        # Si el archivo no existe, sqlite3 lo crea
        self.ruta = ruta
        conexion = sqlite3.connect(self.ruta)
        try:
            conexion.executescript(CREAR_TABLAS)
        finally:
            conexion.close()

    def append(self, inscripcion):
        conexion = sqlite3.connect(self.ruta)
        try:
            # Una sola transacción: se guarda todo o nada
            with conexion:
                cursor = conexion.execute(
                    "INSERT INTO inscripciones (actividad, horario) "
                    "VALUES (?, ?)",
                    (inscripcion.actividad, inscripcion.horario.isoformat()))
                for visitante in inscripcion.visitantes:
                    conexion.execute(
                        "INSERT INTO visitantes (inscripcion_id, nombre, dni, "
                        "edad, talle) VALUES (?, ?, ?, ?, ?)",
                        (cursor.lastrowid, visitante.nombre, visitante.dni,
                         visitante.edad, visitante.talle))
        finally:
            conexion.close()

    def __iter__(self):
        conexion = sqlite3.connect(self.ruta)
        try:
            inscripciones = []
            filas = conexion.execute(
                "SELECT id, actividad, horario FROM inscripciones "
                "ORDER BY id").fetchall()
            for numero, actividad, horario in filas:
                visitantes = []
                for datos in conexion.execute(
                        "SELECT nombre, dni, edad, talle FROM visitantes "
                        "WHERE inscripcion_id = ? ORDER BY id", (numero,)):
                    visitantes.append(Visitante(*datos))
                inscripciones.append(Inscripcion(
                    actividad, datetime.fromisoformat(horario), visitantes))
        finally:
            conexion.close()
        return iter(inscripciones)

    def __len__(self):
        conexion = sqlite3.connect(self.ruta)
        try:
            cursor = conexion.execute("SELECT COUNT(*) FROM inscripciones")
            return cursor.fetchone()[0]
        finally:
            conexion.close()
