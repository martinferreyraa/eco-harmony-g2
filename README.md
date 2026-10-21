# EcoHarmony Park · Inscribirme a actividad

TP6 (TDD) de Ingeniería y Calidad de Software, UTN-FRC, 4K3, Grupo 2.
Implementa la US "Inscribirme a actividad" con Python, pytest y Flask.

## Requisitos

- Python 3.10 o superior (`python --version`).
- Una cuenta de mail con SMTP para el mail de confirmación (por ejemplo,
  Gmail con una contraseña de aplicación).

## Instalación (una sola vez)

```
git clone https://github.com/martinferreyraa/eco-harmony-g2.git
cd eco-harmony-g2
python -m venv .venv
```

Activar el entorno virtual:

- Windows (PowerShell): `.venv\Scripts\Activate.ps1`
- Windows (cmd): `.venv\Scripts\activate.bat`
- Linux / macOS: `source .venv/bin/activate`

Instalar las dependencias:

```
python -m pip install -r requirements.txt
```

## Configurar el mail (`.env`)

Copiar `.env.example` como `.env` y completar los datos reales:

| Variable | Qué es |
|---|---|
| `SMTP_HOST` | Servidor SMTP (por ejemplo, `smtp.gmail.com`) |
| `SMTP_PORT` | Puerto con STARTTLS (normalmente `587`) |
| `SMTP_USER` | Cuenta que envía los mails |
| `SMTP_PASS` | Contraseña de aplicación de esa cuenta |
| `MAIL_USUARIO_MOCK` | Mail que recibe la confirmación (usuario mockeado, FAQ #19) |

`.env` está en el `.gitignore`: nunca se sube al repositorio.
Los tests no lo necesitan, porque no mandan mails reales.

## Correr los tests

```
python -m pytest -v
```

Para un solo archivo: `python -m pytest -v tests/test_seed.py`.

## Levantar la aplicación

```
python -m flask --app web/app run
```

Abrir <http://127.0.0.1:5000> en el navegador. Se corta con `Ctrl + C`.

La primera vez se crea sola la base `eco_harmony.db` en la raíz del
proyecto. Además, al arrancar se llena el próximo turno reservable de Safari,
para mostrar el caso "sin cupo". Para empezar de cero, borrar
`eco_harmony.db` con el servidor apagado.

Si la aplicación corta con "Falta configurar ... en .env", falta el `.env` o
alguna de sus variables.

## Estructura

```
dominio/     reglas de negocio y validaciones (lo que se testea)
servicios/   mail SMTP, imagen del QR y registro en SQLite
web/         Flask: rutas, plantillas y estilos (sin validaciones)
tests/       tests de pytest
Docs/        bitácora TDD (ciclos Red / Green / Refactor y supuestos),
             decisiones de diseño y enunciado del TP6
```
