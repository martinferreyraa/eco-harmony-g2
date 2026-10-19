# CLAUDE.md — TP6 TDD · EcoHarmony Park · "Inscribirme a actividad"

Trabajo práctico evaluable de Ingeniería y Calidad de Software (UTN-FRC, 4K3, Grupo 2).
El objetivo NO es solo que funcione: es demostrar el ciclo TDD (Red → Green → Refactor)
y que el grupo pueda explicar cada línea del código en un oral.

## Ciclo TDD a seguir (el de la cátedra)

Para cada test de la lista, en este orden y de a un test por vez:

1. **Escribir un test.** Solo uno.
2. **Hacer que el test compile.** Si importa algo que no existe, crear lo mínimo
   (una función vacía, por ejemplo) para que pytest pueda ejecutarlo.
3. **Hacer que el test falle (Red).** Correr `pytest` y mostrar el fallo.
4. **Hacer un cambio para que pase.** El código mínimo necesario, nada más.
5. **Correr el test para que pase (Green).** Correr toda la suite: nada se puede romper.
6. **Quitar duplicaciones (Refactor).** Si hay duplicación o algo poco claro,
   mejorarlo sin cambiar el comportamiento y volver a correr los tests.
   Si no hace falta, decirlo y seguir.

Al terminar cada ciclo, explicá en dos o tres líneas simples qué se hizo y por qué
(el grupo tiene que poder repetirlo en un oral). Nunca escribas varios tests juntos
ni implementes funcionalidad por adelantado.

## Principios no negociables

1. **Alcance mínimo.** Solo lo que pide la US, el enunciado del TP6 o el FAQ de los PO.
   No agregar registro, login, contraseñas, pagos ni features extra. Si algo no está
   escrito en esos documentos, preguntá antes de implementarlo.
2. **Código simple.** Funciones cortas, nombres en español y sin abstracciones innecesarias.
   Si hay que elegir entre corto y claro, elegí claro.
3. **Toda validación vive en `dominio/`.** La capa web no valida nada: solo recibe el
   formulario, llama a `inscribir(...)` y muestra el resultado o el mensaje de error.
4. **Un mensaje de error distinto = un test distinto.**

## Stack

- Python 3, `pytest`, `Flask` (con Jinja), `qrcode`, `python-dotenv`.
- Front: HTML + CSS propio, responsive (se prueba con DevTools en modo celular).
  Fuente **Lato** (Google Fonts). Paleta: `#386641`, `#6A994E`, `#A7C957`, `#F2E8CF`, `#BC4749`.
- Sin base de datos: los datos salen de un seed en memoria (`dominio/seed.py`).
- Comandos permitidos en la demo: `pytest` y `flask --app web/app run`.

## Estructura

```
dominio/
  inscripcion.py   # inscribir(...) y validaciones
  reglas.py        # constantes del FAQ
  seed.py          # actividades y turnos iniciales
servicios/
  mail.py          # EnviadorSMTP (real, lee credenciales de .env)
  qr.py            # genera el QR de cada visitante
web/
  app.py           # Flask, capa delgada
  templates/
  static/estilos.css
tests/
  conftest.py      # fixtures: seed limpio, EnviadorFalso, "ahora" fijo
  test_inscripcion.py
.env.example       # SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, MAIL_USUARIO_MOCK
```

`dominio/` nunca importa de `web/`. Los tests solo importan de `dominio/` y `servicios/qr.py`.

## Decisiones de diseño clave

- **"Ahora" inyectado:** `inscribir(..., ahora)` recibe la fecha y hora actual como
  parámetro. Los tests usan un `datetime` fijo; la app pasa `datetime.now()`.
  Sin esto, los tests de horario serían no determinísticos.
- **Enviador inyectado:** `inscribir(..., enviador)`. La app usa `EnviadorSMTP` (mail real),
  y los tests usan `EnviadorFalso`, que guarda lo enviado en una lista. Los tests NUNCA
  mandan mails reales.
- **Usuario mockeado** (FAQ #19): sin registro ni login. El mail destino es
  `MAIL_USUARIO_MOCK` del `.env`.
- **Credenciales:** `.env` está en `.gitignore`. El repo es público, así que solo se sube `.env.example`.
- **Falla del SMTP:** la inscripción queda registrada y se informa que el mail no pudo
  enviarse (decisión del grupo; confirmar antes de implementar).
- **QR:** uno por visitante, adjunto al mail. Se testea QUÉ datos contiene, no la imagen
  (la generación es responsabilidad de la librería `qrcode`).

## Reglas de negocio (fuente entre paréntesis)

- Actividades: Tirolesa, Safari, Palestra, Jardinería (US).
- Cupos por turno: Safari 8, Palestra 12, Jardinería 12, Tirolesa 10 (FAQ #13).
- Turnos: uno por hora, inicios de 9:00 a 17:00. A las 18 no hay turno (FAQ #12).
- Parque abierto de 8:30 a 19 (FAQ #11). Cerrado los lunes, el 25/12 y el 1/1 (FAQ #1).
- Ventana de reserva: desde 24 hs antes hasta 15 min antes del inicio del turno
  (FAQ #23 y #30).
- Requieren talle: Palestra y Tirolesa (FAQ #9). Talles válidos: XS, S, M, L, XL, XXL (FAQ #14).
- Edad mínima: Palestra 12, Tirolesa 8, Safari y Jardinería sin límite (FAQ #15).
- Datos por visitante: nombre, DNI, edad y talle si corresponde (US). Solo DNI, sin pasaporte (FAQ #32).
  Formato del DNI: 7 u 8 dígitos (decisión del grupo, no está escrita en el FAQ).
- Sin máximo de personas por inscripción: el único límite es el cupo (FAQ #31).
- Un mismo DNI no puede estar inscripto en dos actividades en el mismo horario (FAQ #29).
- Hay que aceptar los términos y condiciones específicos de la actividad (US, FAQ #16).
- Mail de confirmación con el resumen de la inscripción y los QR (TP6, FAQ #28).

## Lista de tests (orden sugerido de ciclos)

1. Camino feliz: `test_inscripcion_exitosa`
2. Presencia: `test_no_seleccionar_actividad`, `test_no_seleccionar_horario`,
   `test_nombre_vacio`, `test_dni_vacio`, `test_edad_vacia`, `test_no_acepta_terminos`
3. Formato: `test_dni_invalido`, `test_edad_invalida`
4. Por actividad: `test_talle_requerido_faltante`, `test_talle_no_requerido_omitido`,
   `test_talle_invalido`, `test_edad_menor_minimo_palestra`,
   `test_edad_menor_minimo_tirolesa`, `test_edad_igual_minimo_pasa`,
   `test_safari_sin_limite_edad`
5. Cantidad y cupo: `test_cantidad_cero`, `test_cantidad_no_coincide_con_visitantes`,
   `test_actividad_sin_cupo`, `test_cantidad_supera_cupo_disponible`,
   `test_inscripcion_descuenta_cupo`
6. Tiempo: `test_turno_fuera_de_rango`, `test_dia_lunes_cerrado`,
   `test_dia_feriado_cerrado`, `test_turno_ya_pasado`, `test_reserva_mas_de_24hs_antes`,
   `test_reserva_menos_de_15min_antes`
7. Superposición: `test_dni_inscripto_mismo_horario`
8. Mail y QR: `test_envia_mail_al_confirmar`, `test_no_envia_mail_si_falla`,
   `test_mail_incluye_resumen`, `test_mail_incluye_qr_por_visitante`,
   `test_falla_envio_mail`
9. GUI web (sin tests): formulario, confirmación y estilos.

Estilo de los tests: estructura Arrange / Act / Assert, datos fáciles de leer,
tests independientes entre sí (cada uno arma su propio seed mediante fixture).

## Commits

Un commit por fase del ciclo, para que el historial muestre el TDD:
- `test: agregado test_<nombre> (red)`
- `feat: <comportamiento> (green)`
- `refactor: <qué se mejoró>`
