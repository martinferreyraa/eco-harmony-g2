import pytest

from dominio.inscripcion import ErrorInscripcion, inscribir


def test_inscripcion_exitosa(datos_validos, registro):
    # Arrange: datos_validos ya trae una inscripción correcta

    # Act
    inscribir(**datos_validos)

    # Assert
    assert len(registro) == 1


def test_no_seleccionar_actividad(datos_validos, registro):
    # Arrange
    datos_validos["actividad"] = ""

    # Act y Assert
    with pytest.raises(ErrorInscripcion,
                       match="Debe seleccionar una actividad"):
        inscribir(**datos_validos)
    assert len(registro) == 0


def test_no_seleccionar_horario(datos_validos, registro):
    # Arrange
    datos_validos["horario"] = None

    # Act y Assert
    with pytest.raises(ErrorInscripcion,
                       match="Debe seleccionar un horario"):
        inscribir(**datos_validos)
    assert len(registro) == 0


def test_nombre_vacio(datos_validos, registro):
    # Arrange
    datos_validos["visitantes"][0].nombre = ""

    # Act y Assert
    with pytest.raises(ErrorInscripcion,
                       match="Debe ingresar el nombre de cada visitante"):
        inscribir(**datos_validos)
    assert len(registro) == 0


def test_dni_vacio(datos_validos, registro):
    # Arrange
    datos_validos["visitantes"][0].dni = ""

    # Act y Assert
    with pytest.raises(ErrorInscripcion,
                       match="Debe ingresar el DNI de cada visitante"):
        inscribir(**datos_validos)
    assert len(registro) == 0


def test_edad_vacia(datos_validos, registro):
    # Arrange
    datos_validos["visitantes"][0].edad = ""

    # Act y Assert
    with pytest.raises(ErrorInscripcion,
                       match="Debe ingresar la edad de cada visitante"):
        inscribir(**datos_validos)
    assert len(registro) == 0
