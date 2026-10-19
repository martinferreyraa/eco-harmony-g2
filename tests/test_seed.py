from datetime import datetime

from dominio.inscripcion import Visitante, cupo_disponible, inscribir
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
