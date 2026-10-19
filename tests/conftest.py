from datetime import datetime

import pytest

from dominio.inscripcion import Visitante


@pytest.fixture
def registro():
    return []


@pytest.fixture
def ahora():
    # Martes 20/10/2026 a las 10:00: el parque abre ese día
    return datetime(2026, 10, 20, 10, 0)


@pytest.fixture
def datos_validos(registro, ahora):
    # Safari a las 12:00 del mismo día: 2 hs antes, dentro de la ventana
    return {
        "actividad": "Safari",
        "horario": datetime(2026, 10, 20, 12, 0),
        "cantidad": 1,
        "visitantes": [Visitante("Ana Pérez", "30123456", "25")],
        "acepta_terminos": True,
        "registro": registro,
        "ahora": ahora,
    }
