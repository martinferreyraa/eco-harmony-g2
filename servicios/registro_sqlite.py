import sqlite3
from contextlib import closing
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


def leer_visitantes(conexion, numero):
    """Los visitantes de una inscripción, en el orden en que se cargaron."""
    filas = conexion.execute(
        "SELECT nombre, dni, edad, talle FROM visitantes "
        "WHERE inscripcion_id = ? ORDER BY id", (numero,))
    visitantes = []
    for nombre, dni, edad, talle in filas:
        visitantes.append(Visitante(nombre, dni, edad, talle))
    return visitantes


class RegistroSQLite:
    """Reemplaza a la lista de inscripciones: append, recorrer y contar.

    Abre una conexión por operación porque Flask atiende con hilos y una
    conexión de sqlite3 no se comparte entre hilos.
    """

    def __init__(self, ruta):
        # Si el archivo no existe, sqlite3 lo crea
        self.ruta = ruta
        with self.conectar() as conexion:
            conexion.executescript(CREAR_TABLAS)

    def conectar(self):
        # closing() cierra la conexión al salir del with
        return closing(sqlite3.connect(self.ruta))

    def append(self, inscripcion):
        with self.conectar() as conexion:
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

    def __iter__(self):
        inscripciones = []
        with self.conectar() as conexion:
            filas = conexion.execute(
                "SELECT id, actividad, horario FROM inscripciones "
                "ORDER BY id").fetchall()
            for numero, actividad, horario in filas:
                visitantes = leer_visitantes(conexion, numero)
                inscripciones.append(Inscripcion(
                    actividad, datetime.fromisoformat(horario), visitantes))
        return iter(inscripciones)

    def __len__(self):
        with self.conectar() as conexion:
            cursor = conexion.execute("SELECT COUNT(*) FROM inscripciones")
            return cursor.fetchone()[0]
