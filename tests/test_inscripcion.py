from datetime import datetime

import pytest

from dominio.inscripcion import (ErrorInscripcion, Inscripcion, Visitante,
                                 cupo_disponible, inscribir)


def crear_visitantes(cantidad):
    visitantes = []
    for numero in range(cantidad):
        dni = str(40000000 + numero)
        visitantes.append(Visitante(f"Visitante {numero}", dni, "30"))
    return visitantes


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


def test_edad_menor_minimo_palestra(datos_validos, registro):
    # Arrange
    datos_validos["actividad"] = "Palestra"
    datos_validos["visitantes"][0].talle = "M"
    datos_validos["visitantes"][0].edad = "11"

    # Act y Assert
    with pytest.raises(ErrorInscripcion,
                       match="La edad mínima para Palestra es 12 años"):
        inscribir(**datos_validos)
    assert len(registro) == 0


def test_edad_menor_minimo_tirolesa(datos_validos, registro):
    # Arrange
    datos_validos["actividad"] = "Tirolesa"
    datos_validos["visitantes"][0].talle = "S"
    datos_validos["visitantes"][0].edad = "7"

    # Act y Assert
    with pytest.raises(ErrorInscripcion,
                       match="La edad mínima para Tirolesa es 8 años"):
        inscribir(**datos_validos)
    assert len(registro) == 0


def test_edad_igual_minimo_pasa(datos_validos, registro):
    # Arrange: 12 años es justo el mínimo de Palestra
    datos_validos["actividad"] = "Palestra"
    datos_validos["visitantes"][0].talle = "M"
    datos_validos["visitantes"][0].edad = "12"

    # Act
    inscribir(**datos_validos)

    # Assert
    assert len(registro) == 1


def test_safari_sin_limite_edad(datos_validos, registro):
    # Arrange: Safari no tiene edad mínima
    datos_validos["visitantes"][0].edad = "3"

    # Act
    inscribir(**datos_validos)

    # Assert
    assert len(registro) == 1


def test_cantidad_cero(datos_validos, registro):
    # Arrange
    datos_validos["cantidad"] = 0
    datos_validos["visitantes"] = []

    # Act y Assert
    with pytest.raises(ErrorInscripcion,
                       match="Debe indicar al menos una persona"):
        inscribir(**datos_validos)
    assert len(registro) == 0


def test_cantidad_no_coincide_con_visitantes(datos_validos, registro):
    # Arrange: dice 2 personas pero cargó los datos de 1
    datos_validos["cantidad"] = 2

    # Act y Assert
    with pytest.raises(ErrorInscripcion,
                       match="La cantidad de personas no coincide"):
        inscribir(**datos_validos)
    assert len(registro) == 0


def test_actividad_sin_cupo(datos_validos, registro):
    # Arrange: el turno de Safari ya tiene sus 8 lugares ocupados
    turno_lleno = Inscripcion("Safari", datos_validos["horario"],
                              crear_visitantes(8))
    registro.append(turno_lleno)

    # Act y Assert
    with pytest.raises(ErrorInscripcion,
                       match="No hay cupo disponible para Safari"):
        inscribir(**datos_validos)
    assert len(registro) == 1


def test_cantidad_supera_cupo_disponible(datos_validos, registro):
    # Arrange: quedan 2 lugares en Safari y se quieren anotar 3 personas
    registro.append(Inscripcion("Safari", datos_validos["horario"],
                                crear_visitantes(6)))
    datos_validos["cantidad"] = 3
    datos_validos["visitantes"] = [
        Visitante("Ana Pérez", "30123456", "25"),
        Visitante("Luis Gómez", "31234567", "40"),
        Visitante("Sofía Díaz", "32345678", "10"),
    ]

    # Act y Assert
    with pytest.raises(ErrorInscripcion,
                       match="Solo quedan 2 lugares disponibles"):
        inscribir(**datos_validos)
    assert len(registro) == 1


def test_inscripcion_descuenta_cupo(datos_validos, registro):
    # Arrange
    horario = datos_validos["horario"]

    # Act
    inscribir(**datos_validos)

    # Assert: Safari tiene 8 lugares y se ocupó 1
    assert cupo_disponible("Safari", horario, registro) == 7


@pytest.mark.parametrize("horario", [datetime(2026, 10, 20, 8, 0),
                                     datetime(2026, 10, 20, 18, 0),
                                     datetime(2026, 10, 20, 12, 30)])
def test_turno_fuera_de_rango(datos_validos, registro, horario):
    # Arrange: los turnos empiezan en punto, de 9 a 17
    datos_validos["horario"] = horario

    # Act y Assert
    with pytest.raises(ErrorInscripcion,
                       match="El horario debe ser un turno en punto"):
        inscribir(**datos_validos)
    assert len(registro) == 0


def test_dia_lunes_cerrado(datos_validos, registro):
    # Arrange: el 26/10/2026 es lunes
    datos_validos["horario"] = datetime(2026, 10, 26, 12, 0)

    # Act y Assert
    with pytest.raises(ErrorInscripcion,
                       match="El parque está cerrado los lunes"):
        inscribir(**datos_validos)
    assert len(registro) == 0


@pytest.mark.parametrize("horario", [datetime(2026, 12, 25, 12, 0),
                                     datetime(2027, 1, 1, 12, 0)])
def test_dia_feriado_cerrado(datos_validos, registro, horario):
    # Arrange: el parque cierra el 25/12 y el 1/1
    datos_validos["horario"] = horario

    # Act y Assert
    with pytest.raises(ErrorInscripcion,
                       match="El parque está cerrado el 25/12 y el 1/1"):
        inscribir(**datos_validos)
    assert len(registro) == 0


def test_turno_ya_pasado(datos_validos, registro):
    # Arrange: son las 10:00 y el turno de las 9:00 ya empezó
    datos_validos["horario"] = datetime(2026, 10, 20, 9, 0)

    # Act y Assert
    with pytest.raises(ErrorInscripcion,
                       match="El turno seleccionado ya pasó"):
        inscribir(**datos_validos)
    assert len(registro) == 0


def test_reserva_mas_de_24hs_antes(datos_validos, registro):
    # Arrange: son las 10:00 del martes y el turno es el miércoles a las 11
    datos_validos["horario"] = datetime(2026, 10, 21, 11, 0)

    # Act y Assert
    with pytest.raises(ErrorInscripcion,
                       match="Solo se puede reservar desde 24 hs antes"):
        inscribir(**datos_validos)
    assert len(registro) == 0


def test_reserva_menos_de_15min_antes(datos_validos, registro):
    # Arrange: son las 11:50 y el turno es a las 12:00
    datos_validos["ahora"] = datetime(2026, 10, 20, 11, 50)

    # Act y Assert
    with pytest.raises(ErrorInscripcion,
                       match="Se debe reservar al menos 15 minutos antes"):
        inscribir(**datos_validos)
    assert len(registro) == 0


def test_reserva_justo_24hs_antes_pasa(datos_validos, registro):
    # Arrange: martes 12:00 y el turno es el miércoles 12:00 (24 hs justas)
    datos_validos["ahora"] = datetime(2026, 10, 20, 12, 0)
    datos_validos["horario"] = datetime(2026, 10, 21, 12, 0)

    # Act
    inscribir(**datos_validos)

    # Assert
    assert len(registro) == 1


def test_reserva_justo_15min_antes_pasa(datos_validos, registro):
    # Arrange: son las 11:45 y el turno es a las 12:00 (15 min justos)
    datos_validos["ahora"] = datetime(2026, 10, 20, 11, 45)

    # Act
    inscribir(**datos_validos)

    # Assert
    assert len(registro) == 1


def test_dni_inscripto_mismo_horario(datos_validos, registro):
    # Arrange: Ana ya está inscripta en Tirolesa a la misma hora
    ana = Visitante("Ana Pérez", "30123456", "25", "M")
    registro.append(Inscripcion("Tirolesa", datos_validos["horario"], [ana]))

    # Act y Assert
    with pytest.raises(ErrorInscripcion,
                       match="El DNI 30123456 ya tiene una inscripción"):
        inscribir(**datos_validos)
    assert len(registro) == 1


def test_envia_mail_al_confirmar(datos_validos, enviador):
    # Act
    inscribir(**datos_validos)

    # Assert
    assert len(enviador.enviados) == 1


def test_no_envia_mail_si_validacion_falla(datos_validos, enviador):
    # Arrange: un dato inválido (no acepta los términos)
    datos_validos["acepta_terminos"] = False

    # Act
    with pytest.raises(ErrorInscripcion):
        inscribir(**datos_validos)

    # Assert
    assert enviador.enviados == []


def test_mail_incluye_resumen(datos_validos, enviador):
    # Arrange
    datos_validos["actividad"] = "Palestra"
    datos_validos["visitantes"][0].talle = "M"

    # Act
    inscribir(**datos_validos)

    # Assert
    cuerpo = enviador.enviados[0].cuerpo
    assert "Actividad: Palestra" in cuerpo
    assert "Fecha y hora: 20/10/2026 12:00" in cuerpo
    assert "Cantidad de personas: 1" in cuerpo
    assert "Ana Pérez, DNI 30123456, 25 años, talle M" in cuerpo
