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
