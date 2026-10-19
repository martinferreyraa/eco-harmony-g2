from datetime import datetime

import pytest

from dominio.inscripcion import Visitante


@pytest.fixture
def registro():
    return []


@pytest.fixture
def datos_validos(registro):
    return {
        "actividad": "Safari",
        "horario": datetime(2026, 10, 20, 12, 0),
        "cantidad": 1,
        "visitantes": [Visitante("Ana Pérez", "30123456", "25")],
        "acepta_terminos": True,
        "registro": registro,
    }
