from datetime import datetime

import pytest

from dominio.inscripcion import Visitante


class EnviadorFalso:
    """Reemplaza al SMTP en los tests: guarda los mails en vez de enviarlos."""

    def __init__(self):
        self.enviados = []

    def enviar(self, mail):
        self.enviados.append(mail)


class EnviadorQueFalla:
    """Simula que el servidor de mail no responde."""

    def enviar(self, mail):
        raise ConnectionError("El servidor de mail no responde")


@pytest.fixture
def enviador():
    return EnviadorFalso()


@pytest.fixture
def enviador_que_falla():
    return EnviadorQueFalla()


@pytest.fixture
def registro():
    return []


@pytest.fixture
def ahora():
    # Martes 20/10/2026 a las 10:00: el parque abre ese día
    return datetime(2026, 10, 20, 10, 0)


@pytest.fixture
def datos_validos(registro, ahora, enviador):
    # Safari a las 12:00 del mismo día: 2 hs antes, dentro de la ventana
    return {
        "actividad": "Safari",
        "horario": datetime(2026, 10, 20, 12, 0),
        "cantidad": 1,
        "visitantes": [Visitante("Ana Pérez", "30123456", "25")],
        "acepta_terminos": True,
        "registro": registro,
        "ahora": ahora,
        "enviador": enviador,
    }
