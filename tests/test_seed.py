from datetime import datetime

from dominio.inscripcion import (Inscripcion, Visitante, cupo_disponible,
                                 inscribir)
from dominio.seed import crear_seed


def test_seed_llena_el_proximo_turno_reservable_de_safari(registro, ahora,
                                                          enviador):
    # Arrange: ahora es martes 10:00; el próximo turno reservable es 11:00
    proximo_turno = datetime(2026, 10, 20, 11, 0)

    # Act
    crear_seed(registro, ahora)

    # Assert: Safari está lleno en ese turno...
    assert registro[0].horario == proximo_turno
    assert cupo_disponible("Safari", proximo_turno, registro) == 0
    # ...y el turno está en la ventana: otra actividad se puede reservar
    visitante = Visitante("Ana Pérez", "30123456", "25")
    inscribir("Jardinería", proximo_turno, 1, [visitante], True,
              registro, ahora, enviador)
    assert len(registro) == 2


def test_seed_no_duplica_el_turno_lleno(registro, ahora):
    # Arrange: la app ya arrancó una vez y el turno quedó lleno
    proximo_turno = datetime(2026, 10, 20, 11, 0)
    crear_seed(registro, ahora)

    # Act: la app arranca de nuevo con la misma base
    crear_seed(registro, ahora)

    # Assert
    assert len(registro) == 1
    assert cupo_disponible("Safari", proximo_turno, registro) == 0


def test_seed_completa_el_turno_con_lugares_ocupados(registro, ahora):
    # Arrange: 3 personas ya se anotaron en el turno de las 11
    proximo_turno = datetime(2026, 10, 20, 11, 0)
    visitantes = [Visitante("Ana Pérez", "30123456", "25"),
                  Visitante("Juan Gómez", "31123456", "30"),
                  Visitante("Rosa Díaz", "32123456", "40")]
    registro.append(Inscripcion("Safari", proximo_turno, visitantes))

    # Act
    crear_seed(registro, ahora)

    # Assert: agrega solo los 5 lugares que faltaban
    assert len(registro[1].visitantes) == 5
    assert cupo_disponible("Safari", proximo_turno, registro) == 0
