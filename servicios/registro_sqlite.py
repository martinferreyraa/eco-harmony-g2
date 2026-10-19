class RegistroSQLite:

    def __init__(self, ruta):
        self.ruta = ruta
        self.inscripciones = []

    def append(self, inscripcion):
        self.inscripciones.append(inscripcion)

    def __iter__(self):
        return iter(self.inscripciones)
