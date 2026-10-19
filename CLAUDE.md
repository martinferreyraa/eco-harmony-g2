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
5. **Estilo de código: PEP 8** (reglas de estilo elegidas por el grupo en el TP2; el
   enunciado del TP6 exige respetarlas). Nombres de funciones y variables en `snake_case`,
   constantes en `MAYUSCULAS`, líneas de 79 caracteres como máximo, 4 espacios de sangría.

## Términos y condiciones

Redactá vos un texto de términos y condiciones distinto para cada actividad (FAQ #16),
de 3 o 4 líneas como máximo cada uno, en lenguaje simple y adecuado al riesgo de la actividad
(por ejemplo, Tirolesa: uso obligatorio del arnés y de las indicaciones del instructor).
Guardalos en `dominio/reglas.py` como un diccionario `TERMINOS = {actividad: texto}`.
La GUI los muestra antes del checkbox de aceptación. El grupo los revisa antes de
enviarlos a validar a los PO.

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
Redactando preguntas de defensa y notas finales antes del mensaje.
El plan está bien armado, y el DNI repetido ya figura como ciclo 9, que es lo que querías. Antes de aprobarlo encontré un bug y tres huecos.

1. Bug en el fixture. datos_validos usa “mañana 11:00” con ahora = martes 10:00, o sea 25 hs. La regla del FAQ #23 solo deja reservar dentro de las 24 hs. Cuando llegue el ciclo 6, todos los tests anteriores se ponen rojos juntos por algo que no tiene que ver con lo que prueban. Conviene que el horario base sea el mismo día a las 12:00.

2. Los límites inclusivos no tienen test. El plan asume que exactamente 24 hs y exactamente 15 min pasan, pero el ciclo 6 solo trae “más de 24 hs” y “menos de 15 min”. Con solo esos dos, tanto < como <= los pasan, así que nada fija la decisión. Hacen falta dos tests de borde:

24 hs: con ahora = martes 10:00, el turno del miércoles 10:00 pasa y el de las 11:00 falla.
15 min: con ahora = 9:45, el turno de las 10:00 pasa.
El FAQ no dice si el límite entra, así que va al documento como decisión del grupo.

3. Falta test_edad_cero_valida. El plan define 0 a 120, pero nada prueba que el 0 pase. Es justo el caso que rompe if not edad una vez convertida a int.

4. Las decisiones de la sesión no están en el CLAUDE.md. La edad de 0 a 120 y la ventana inclusiva viven solo en esa conversación. Si abren una sesión nueva, Claude Code las pierde. El plan solo propone actualizar el CLAUDE.md con el DNI repetido.

Sobre el DNI repetido: el ciclo 7 ya cubre el mismo DNI en dos inscripciones distintas. El ciclo 9 cubre solo el repetido dentro del mismo formulario. Se justifica por el FAQ #29: una persona no puede ocupar dos lugares en el mismo turno. En el documento figura como derivada de esa regla, no inventada.

Preguntas de oral que ya se ven venir:

¿Por qué inscribir tiene 8 parámetros? Cada uno es una entrada o una dependencia inyectada (registro, enviador, ahora).
¿Por qué except Exception al enviar? Solo envuelve la llamada a enviar, así que no esconde errores propios.
EnviadorSMTP e imagen_qr no tienen tests: se verifican a mano en la demo. Aclaralo en el documento.
Para el ciclo 10, el FAQ #2 dice que un día cerrado debería verse deshabilitado en el calendario, o no dejar elegirlo. Un input type=date común deja elegir lunes y el dominio lo rechaza con mensaje. Decidan si eso les alcanza o suman un poco de JS.

Este es el mensaje para responderle:

Plan aprobado con estos cambios:

1. Fixture: "mañana 11:00" queda a 25 hs de `ahora` (martes 10:00) y violaría la regla de 24 hs. Usá el mismo día a las 12:00 como horario base.
2. La ventana de reserva es inclusiva. Agregá al ciclo 6 los tests `test_reserva_justo_24hs_antes_pasa` y `test_reserva_justo_15min_antes_pasa`. Cada uno arma su propio `ahora`.
3. Agregá `test_edad_cero_valida` (Safari, edad "0") al ciclo 3.
4. Antes del ciclo 0 actualizá CLAUDE.md con: el grupo 9 (DNI repetido, decisión del grupo, la GUI pasa a 10), los tres tests nuevos, y estas decisiones en las reglas de negocio: edad válida = entero entre 0 y 120; ventana de reserva inclusiva; el talle enviado a una actividad que no lo requiere se ignora.

Después arrancamos con el ciclo 0.
pasted-content-id-c2ec-desarrollaremos-reactive-lerdorf.md
pasted-content-id-c2ec-desarrollaremos-reactiv
e-lerdorf
.md
MD
Ajustando la semilla de datos para que no quede obsoleta.
El plan incorporó los cuatro cambios que pedimos, así que está listo para aprobar. Solo le haría tres ajustes chicos, y el primero conviene resolverlo antes del ciclo 10.

1. El seed con fecha fija se vence. Dice que el seed deja “un turno de Safari ya lleno” para mostrar el caso sin cupo. Si esa fecha queda escrita a mano, el día de la demo ya pasó o cae fuera de la ventana de 24 hs, y el caso no se puede mostrar. El seed tiene que armarse a partir de la hora actual (ahora) y no de una fecha escrita. Por la misma regla de las 24 hs, la demo solo funciona un día en que el parque abra, así que no la hagan un domingo a la noche ni un lunes, porque no hay ningún turno reservable.

2. El nombre de un test es confuso. test_no_envia_mail_si_falla suena a “si falla el envío”, pero el plan lo usa para “si falla la validación”. Junto a test_falla_envio_mail_no_inscribe, un profe puede confundirse. Lo renombraría a test_no_envia_mail_si_validacion_falla.

3. Sin el FAQ en disco, Claude Code se apoya solo en el CLAUDE.md. El plan lo dice y está bien. Pero si más adelante duda de una regla que no figura ahí (por ejemplo, qué pasa con el cierre del parque a las 19), tiene que preguntarles y no suponer. Se lo pediría explícito.

Todo lo demás lo veo bien: el fixture ya no rompe la regla de las 24 hs, los bordes inclusivos tienen test, y el DNI repetido quedó al final como acordaron.

Mensaje para responderle:

Plan aprobado, con tres ajustes:

1. Renombrá test_no_envia_mail_si_falla a test_no_envia_mail_si_validacion_falla (en el plan y en el CLAUDE.md).
2. El seed no puede tener fechas escritas a mano: en el ciclo 10 tiene que armarse a partir de la hora actual, para que el caso "sin cupo" se pueda mostrar el día de la demo.
3. Si necesitás una regla que no está en el CLAUDE.md (el FAQ no está en disco), preguntame y no supongas.

Empezá: actualizá el CLAUDE.md, hacé el ciclo 0 y escribí 

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
- **Falla del SMTP:** si el mail no se puede enviar, la inscripción NO se realiza
  (el CA dice que "se debe enviar" el correo al finalizar). Orden en `inscribir(...)`:
  validar todo → enviar el mail → recién después registrar la inscripción y descontar
  el cupo. Si el envío falla, se lanza un error y el cupo queda intacto.
- **QR:** uno por visitante, adjunto al mail. Se testea QUÉ datos contiene, no la imagen
  (la generación es responsabilidad de la librería `qrcode`).

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
  Formato del DNI: solo dígitos, sin puntos ni espacios, 7 u 8 caracteres
  (convención habitual en sistemas argentinos; decisión del grupo).
  Edad válida: número entero entre 0 y 120 (decisión del grupo).
- Un mismo DNI no puede aparecer dos veces en la misma inscripción (decisión del grupo).
- Sin máximo de personas por inscripción: el único límite es el cupo (FAQ #31).
- Un mismo DNI no puede estar inscripto en dos actividades en el mismo horario (FAQ #29).
- Hay que aceptar los términos y condiciones específicos de la actividad (US, FAQ #16).
- Mail de confirmación con el resumen de la inscripción y los QR (TP6, FAQ #28).

## Lista de tests (orden sugerido de ciclos)

1. Camino feliz: `test_inscripcion_exitosa`
2. Presencia: `test_no_seleccionar_actividad`, `test_no_seleccionar_horario`,
   `test_nombre_vacio`, `test_dni_vacio`, `test_edad_vacia`, `test_no_acepta_terminos`
3. Formato: `test_dni_invalido`, `test_edad_invalida`, `test_edad_cero_valida`
4. Por actividad: `test_talle_requerido_faltante`, `test_talle_no_requerido_omitido`,
   `test_talle_invalido`, `test_edad_menor_minimo_palestra`,
   `test_edad_menor_minimo_tirolesa`, `test_edad_igual_minimo_pasa`,
   `test_safari_sin_limite_edad`
5. Cantidad y cupo: `test_cantidad_cero`, `test_cantidad_no_coincide_con_visitantes`,
   `test_actividad_sin_cupo`, `test_cantidad_supera_cupo_disponible`,
   `test_inscripcion_descuenta_cupo`
6. Tiempo: `test_turno_fuera_de_rango`, `test_dia_lunes_cerrado`,
   `test_dia_feriado_cerrado`, `test_turno_ya_pasado`, `test_reserva_mas_de_24hs_antes`,
   `test_reserva_menos_de_15min_antes`, `test_reserva_justo_24hs_antes_pasa`,
   `test_reserva_justo_15min_antes_pasa`
7. Superposición: `test_dni_inscripto_mismo_horario`
8. Mail y QR: `test_envia_mail_al_confirmar`,
   `test_no_envia_mail_si_validacion_falla`,
   `test_mail_incluye_resumen`, `test_mail_incluye_qr_por_visitante`,
   `test_falla_envio_mail_no_inscribe` (no se registra y el cupo no se descuenta)
9. DNI repetido en la misma inscripción (decisión del grupo):
   `test_dni_repetido_misma_inscripcion`
10. GUI web (sin tests): formulario, confirmación y estilos. El seed se arma a
    partir de la hora actual (sin fechas escritas a mano).

Estilo de los tests: estructura Arrange / Act / Assert, datos fáciles de leer,
tests independientes entre sí (cada uno arma su propio seed mediante fixture).

## Commits

Un commit por fase del ciclo, para que el historial muestre el TDD:
- `test: agregado test_<nombre> (red)`
- `feat: <comportamiento> (green)`
- `refactor: <qué se mejoró>`
