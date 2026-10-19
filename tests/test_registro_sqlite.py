from datetime import datetime

from dominio.inscripcion import Inscripcion, Visitante
from servicios.registro_sqlite import RegistroSQLite


def inscripcion_de_palestra():
    visitantes = [Visitante("Ana Pérez", "30123456", "25", "M"),
                  Visitante("Juan Gómez", "31123456", "30", "L")]
    return Inscripcion("Palestra", datetime(2026, 10, 20, 12, 0), visitantes)


def test_registro_guarda_y_lee_una_inscripcion(tmp_path):
    # Arrange: el archivo todavía no existe
    registro = RegistroSQLite(tmp_path / "parque.db")
    inscripcion = inscripcion_de_palestra()

    # Act
    registro.append(inscripcion)

    # Assert: vuelve igual, con la fecha y el talle de cada visitante
    assert list(registro) == [inscripcion]


def test_registro_cuenta_inscripciones(tmp_path):
    # Arrange
    registro = RegistroSQLite(tmp_path / "parque.db")

    # Act
    registro.append(inscripcion_de_palestra())
    registro.append(inscripcion_de_palestra())

    # Assert
    assert len(registro) == 2


def test_otra_instancia_ve_lo_guardado(tmp_path):
    # Arrange: como si la app se reiniciara entre una y otra
    ruta = tmp_path / "parque.db"
    inscripcion = inscripcion_de_palestra()
    RegistroSQLite(ruta).append(inscripcion)

    # Act
    otro_registro = RegistroSQLite(ruta)

    # Assert
    assert list(otro_registro) == [inscripcion]
    assert len(otro_registro) == 1
