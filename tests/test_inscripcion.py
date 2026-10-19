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


def test_no_acepta_terminos(datos_validos, registro):
    # Arrange
    datos_validos["acepta_terminos"] = False

    # Act y Assert
    with pytest.raises(ErrorInscripcion,
                       match="Debe aceptar los términos y condiciones"):
        inscribir(**datos_validos)
    assert len(registro) == 0


def test_actividad_inexistente(datos_validos, registro):
    # Arrange
    datos_validos["actividad"] = "Buceo"

    # Act y Assert
    with pytest.raises(ErrorInscripcion,
                       match="La actividad seleccionada no existe"):
        inscribir(**datos_validos)
    assert len(registro) == 0


@pytest.mark.parametrize("dni", ["12.345.678", "123456", "123456789",
                                 "12A45678", "30 123 456"])
def test_dni_invalido(datos_validos, registro, dni):
    # Arrange
    datos_validos["visitantes"][0].dni = dni

    # Act y Assert
    with pytest.raises(ErrorInscripcion,
                       match="El DNI debe tener 7 u 8 dígitos"):
        inscribir(**datos_validos)
    assert len(registro) == 0


@pytest.mark.parametrize("edad", ["abc", "-1", "2.5", "121"])
def test_edad_invalida(datos_validos, registro, edad):
    # Arrange
    datos_validos["visitantes"][0].edad = edad

    # Act y Assert
    with pytest.raises(ErrorInscripcion,
                       match="La edad debe ser un número entero"):
        inscribir(**datos_validos)
    assert len(registro) == 0


def test_edad_cero_valida(datos_validos, registro):
    # Arrange: un bebé puede ir al Safari
    datos_validos["visitantes"][0].edad = "0"

    # Act
    inscribir(**datos_validos)

    # Assert
    assert len(registro) == 1


def test_talle_requerido_faltante(datos_validos, registro):
    # Arrange: Palestra requiere talle y el visitante no lo trae
    datos_validos["actividad"] = "Palestra"

    # Act y Assert
    with pytest.raises(ErrorInscripcion,
                       match="Palestra requiere el talle de cada visitante"):
        inscribir(**datos_validos)
    assert len(registro) == 0


def test_talle_no_requerido_omitido(datos_validos, registro):
    # Arrange: Jardinería no requiere talle y el visitante no lo trae
    datos_validos["actividad"] = "Jardinería"

    # Act
    inscribir(**datos_validos)

    # Assert
    assert len(registro) == 1


def test_talle_invalido(datos_validos, registro):
    # Arrange
    datos_validos["actividad"] = "Palestra"
    datos_validos["visitantes"][0].talle = "XXXL"

    # Act y Assert
    with pytest.raises(ErrorInscripcion, match="El talle debe ser uno de"):
        inscribir(**datos_validos)
    assert len(registro) == 0
