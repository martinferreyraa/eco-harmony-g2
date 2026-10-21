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
5. **Estilo de código: PEP 8** (convención estándar de Python; el TP2 no definió
   reglas propias). Nombres de funciones y variables en `snake_case`,
   constantes en `MAYUSCULAS`, líneas de 79 caracteres como máximo, 4 espacios de sangría.

## Términos y condiciones

Redactá vos un texto de términos y condiciones distinto para cada actividad (FAQ #16),
de 3 o 4 líneas como máximo cada uno, en lenguaje simple y adecuado al riesgo de la actividad
(por ejemplo, Tirolesa: uso obligatorio del arnés y de las indicaciones del instructor).
Guardalos en `dominio/reglas.py` como un diccionario `TERMINOS = {actividad: texto}`.
La GUI los muestra antes del checkbox de aceptación. El grupo los revisa antes de
enviarlos a validar a los PO.

## Stack

- Python 3, `pytest`, `Flask` (con Jinja), `qrcode`, `python-dotenv`,
  `sqlite3` (de la librería estándar).
- Front: HTML + CSS propio, responsive (se prueba con DevTools en modo celular).
  Fuente **Lato** (Google Fonts). Paleta: `#386641`, `#6A994E`, `#A7C957`, `#F2E8CF`, `#BC4749`.
- Base de datos SQLite en `eco_harmony.db` (raíz del proyecto, ignorada por git;
  se crea sola si no existe). En cada arranque, `crear_seed` llena el próximo
  turno reservable de Safari si no está lleno (es idempotente: no lo duplica).
- Comandos permitidos en la demo: `pytest` y `flask --app web/app run`.

## Estructura

```
dominio/
  inscripcion.py   # inscribir(...) y validaciones
  reglas.py        # constantes del FAQ
  seed.py          # actividades y turnos iniciales
servicios/
  mail.py          # EnviadorSMTP (real, lee credenciales de .env)
  qr.py            # convierte el texto del QR en imagen (sin test)
  registro_sqlite.py  # RegistroSQLite: guarda las inscripciones en SQLite
web/
  app.py           # Flask, capa delgada
  templates/
  static/estilos.css
tests/
  conftest.py      # fixtures: seed limpio, EnviadorFalso, "ahora" fijo
  test_inscripcion.py
  test_seed.py
  test_registro_sqlite.py  # con archivos temporales (tmp_path)
.env.example       # SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, MAIL_USUARIO_MOCK
```

`dominio/` nunca importa de `web/` ni de `servicios/`. Los tests solo importan de
`dominio/` y de `servicios/registro_sqlite.py`.

## Decisiones de diseño clave

- **"Ahora" inyectado:** `inscribir(..., ahora)` recibe la fecha y hora actual como
  parámetro. Los tests usan un `datetime` fijo; la app pasa `datetime.now()`.
  Sin esto, los tests de horario serían no determinísticos.
- **Enviador inyectado:** `inscribir(..., enviador)`. La app usa `EnviadorSMTP` (mail real),
  y los tests usan `EnviadorFalso`, que guarda lo enviado en una lista. Los tests NUNCA
  mandan mails reales.
- **Registro inyectado:** `inscribir(..., registro)` solo usa `append`, recorrerlo
  y `len`. Los tests pasan una lista; la app pasa `RegistroSQLite(ruta)`, que tiene
  esas tres operaciones sobre dos tablas (`inscripciones` y `visitantes`). Cada
  `append` guarda la inscripción y sus visitantes en una sola transacción, y cada
  operación abre y cierra su conexión (Flask atiende con hilos).
- **Usuario mockeado** (FAQ #19): sin registro ni login. El mail destino es
  `MAIL_USUARIO_MOCK` del `.env`.
- **Credenciales:** `.env` está en `.gitignore`. El repo es público, así que solo se sube `.env.example`.
- **Falla del SMTP:** si el mail no se puede enviar, la inscripción NO se realiza
  (el CA dice que "se debe enviar" el correo al finalizar). Orden en `inscribir(...)`:
  validar todo → enviar el mail → recién después registrar la inscripción y descontar
  el cupo. Si el envío falla, se lanza un error y el cupo queda intacto.
- **Errores con campo:** `ErrorInscripcion(mensaje, campo)`. El campo dice dónde mostrar
  el error en la GUI: `actividad`, `horario`, `cantidad`, `terminos` o el dato del
  visitante N (`nombre-N`, `dni-N`, `edad-N`, `talle-N`, contando desde 0). Si el error
  no es de un campo (falla del mail), `campo` es `None` y se muestra arriba.
  Se informa un error a la vez (el primero que se encuentra).
- **QR:** uno por visitante, adjunto al mail. `texto_qr` vive en `dominio/inscripcion.py`
  y se testea QUÉ datos contiene, no la imagen. `servicios/qr.py` solo tiene `imagen_qr`
  (lo único que usa la librería `qrcode`), sin test: se verifica a mano en la demo.
- **Número de orden:** `len(registro) + 1`, calculado antes del `append`. Aparece en el
  resumen del mail y en el texto de cada QR.

## Flujo de pantallas

1. **Inicio (`/`)**: actividad, fecha, hora y cantidad, en ese orden. El JS de días
   cerrados avisa si se elige un lunes, el 25/12 o el 1/1 (lee los días de `reglas.py`).
   **Continuar** (`GET /inscripcion`) llama a `validar_reserva` con el registro y
   `datetime.now()`: los errores salen bajo actividad, hora o cantidad.
2. **Formulario (`GET /inscripcion`)**: recibe actividad, fecha, hora y cantidad como
   campos ocultos y muestra el turno como texto, con el link "cambiar turno o cantidad"
   que vuelve al inicio con los valores cargados. Pide los datos de cada visitante y
   la aceptación de los términos de la actividad.
3. **Confirmar (`POST /inscripcion`)**: llama a `inscribir`, que revalida todo. Si falla
   en actividad, horario o cantidad (por ejemplo, el cupo se llenó mientras tanto),
   vuelve al inicio con el error bajo su campo; si falla en un visitante o en los
   términos, vuelve al formulario. Si sale bien, muestra la confirmación.
4. **Cupos (`/cupos`)**: tabla de horas x actividades para una fecha (FAQ #8).

## Reglas de negocio (fuente entre paréntesis)

- Actividades: Tirolesa, Safari, Palestra, Jardinería (US).
- Cupos por turno: Safari 8, Palestra 12, Jardinería 12, Tirolesa 10 (FAQ #13).
- Turnos: uno por hora, inicios de 9:00 a 17:00. A las 18 no hay turno (FAQ #12).
- Parque abierto de 8:30 a 19 (FAQ #11). Cerrado los lunes, el 25/12 y el 1/1 (FAQ #1).
- Ventana de reserva: desde 24 hs antes hasta 15 min antes del inicio del turno
  (FAQ #23 y #30). Es inclusiva: exactamente 24 hs antes y exactamente 15 min
  antes se permiten (decisión del grupo).
- Requieren talle: Palestra y Tirolesa (FAQ #9). Talles válidos: XS, S, M, L, XL, XXL (FAQ #14).
  Si se envía talle a una actividad que no lo requiere, se ignora (decisión del grupo).
- Edad mínima: Palestra 12, Tirolesa 8, Safari y Jardinería sin límite (FAQ #15).
- Datos por visitante: nombre, DNI, edad y talle si corresponde (US). Solo DNI, sin pasaporte (FAQ #32).
  Formato del DNI: solo dígitos (0 a 9), sin puntos ni espacios, 7 u 8 caracteres y
  sin ceros adelante, o sea un número entre 1.000.000 y 99.999.999
  (convención habitual en sistemas argentinos; decisión del grupo).
  Edad válida: número entero entre 0 y 120 (decisión del grupo).
  Nombre completo: al menos dos palabras de al menos 2 letras cada una. Solo letras
  (con tildes y ñ), apóstrofo y guion dentro de las palabras, y espacios entre ellas.
  Sin números, símbolos ni puntos (decisión del grupo).
- Un mismo DNI no puede aparecer dos veces en la misma inscripción (decisión del grupo).
- Sin máximo de personas por inscripción: el único límite es el cupo (FAQ #31).
- Un mismo DNI no puede estar inscripto en dos actividades en el mismo horario (FAQ #29).
- El visitante puede ver los cupos disponibles de cada actividad y turno (FAQ #8).
- Hay que aceptar los términos y condiciones específicos de la actividad (US, FAQ #16).
- Mail de confirmación con número de orden, detalle de visitantes y un QR por visitante
  (TP6, FAQ #18 y #28). Los subtotales y el total del FAQ #18 no aplican: ninguna fuente
  le pone precio a las actividades.
  El QR de cada visitante lleva nombre, DNI, actividad, fecha y hora, y número de orden.

## Lista de tests (orden sugerido de ciclos)

1. Camino feliz: `test_inscripcion_exitosa`
2. Presencia: `test_no_seleccionar_actividad`, `test_no_seleccionar_horario`,
   `test_nombre_vacio`, `test_dni_vacio`, `test_edad_vacia`, `test_no_acepta_terminos`,
   `test_actividad_inexistente` (decisión del grupo; cuando exista `ACTIVIDADES`
   en `reglas.py`; mensaje distinto al de "no seleccionó actividad")
3. Formato: `test_dni_invalido`, `test_edad_invalida`, `test_edad_cero_valida`,
   `test_nombre_invalido` (decisión del grupo)
4. Por actividad: `test_talle_requerido_faltante`, `test_talle_no_requerido_omitido`,
   `test_talle_invalido`, `test_edad_menor_minimo_palestra`,
   `test_edad_menor_minimo_tirolesa`, `test_edad_igual_minimo_pasa`,
   `test_safari_sin_limite_edad`,
   `test_talle_invalido_se_ignora_si_la_actividad_no_lo_requiere` (borde)
5. Cantidad y cupo: `test_cantidad_cero`, `test_cantidad_no_coincide_con_visitantes`,
   `test_actividad_sin_cupo`, `test_cantidad_supera_cupo_disponible`,
   `test_inscripcion_descuenta_cupo`,
   `test_cantidad_igual_al_cupo_restante_pasa` (borde)
6. Tiempo: `test_turno_fuera_de_rango`, `test_dia_lunes_cerrado`,
   `test_dia_feriado_cerrado`, `test_turno_ya_pasado`, `test_reserva_mas_de_24hs_antes`,
   `test_reserva_menos_de_15min_antes`, `test_reserva_justo_24hs_antes_pasa`,
   `test_reserva_justo_15min_antes_pasa`,
   `test_turno_primero_y_ultimo_validos` (borde)
7. Superposición: `test_dni_inscripto_mismo_horario`,
   `test_mismo_dni_en_otro_horario_pasa` (borde)
8. Mail y QR: `test_envia_mail_al_confirmar`,
   `test_no_envia_mail_si_validacion_falla`,
   `test_mail_incluye_resumen`, `test_mail_incluye_numero_de_orden`,
   `test_mail_incluye_qr_por_visitante`,
   `test_falla_envio_mail_no_inscribe` (no se registra y el cupo no se descuenta)
9. DNI repetido en la misma inscripción (decisión del grupo):
   `test_dni_repetido_misma_inscripcion`
10. GUI web (sin tests): formulario, confirmación y estilos. El seed se arma a
    partir de la hora actual (sin fechas escritas a mano).
11. Persistencia en SQLite (decisión del grupo):
    `test_registro_guarda_y_lee_una_inscripcion`, `test_registro_cuenta_inscripciones`,
    `test_otra_instancia_ve_lo_guardado`, `test_seed_no_duplica_el_turno_lleno`,
    `test_seed_completa_el_turno_con_lugares_ocupados`

Estilo de los tests: estructura Arrange / Act / Assert, datos fáciles de leer,
tests independientes entre sí (cada uno arma su propio seed mediante fixture).

## Commits

Un commit por fase del ciclo, para que el historial muestre el TDD:
- `test: agregado test_<nombre> (red)`
- `feat: <comportamiento> (green)`
- `refactor: <qué se mejoró>`
