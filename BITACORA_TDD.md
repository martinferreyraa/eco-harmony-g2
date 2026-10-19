# Bitácora TDD — Inscribirme a actividad

| # | Test | Red | Green | Refactor |
|---|------|-----|-------|----------|
| 1 | `test_inscripcion_exitosa` | `inscribir` era una función vacía y no registraba nada: `assert 0 == 1`. | Se creó el dataclass `Inscripcion` e `inscribir` la agrega a `registro`. | No hizo falta. |
| 2 | `test_no_seleccionar_actividad` | Con la actividad vacía, `inscribir` la registraba igual: `DID NOT RAISE ErrorInscripcion`. | `inscribir` lanza `ErrorInscripcion("Debe seleccionar una actividad")` si la actividad está vacía. | No hizo falta. |
| 3 | `test_no_seleccionar_horario` | Con el horario en `None`, `inscribir` registraba igual: `DID NOT RAISE ErrorInscripcion`. | `inscribir` lanza `ErrorInscripcion("Debe seleccionar un horario")` si el horario está vacío. | No hizo falta (se espera a que se repita el patrón). |
| 4 | `test_nombre_vacio` | Un visitante sin nombre se registraba igual: `DID NOT RAISE ErrorInscripcion`. | `inscribir` recorre los visitantes y lanza error si alguno no tiene nombre. | No hizo falta. |
| 5 | `test_dni_vacio` | Un visitante sin DNI se registraba igual: `DID NOT RAISE ErrorInscripcion`. | Dentro del mismo recorrido se agregó el chequeo del DNI vacío. | No hizo falta. |
| 6 | `test_edad_vacia` | Un visitante sin edad se registraba igual: `DID NOT RAISE ErrorInscripcion`. | Dentro del mismo recorrido se agregó el chequeo de la edad vacía. | No hizo falta (se refactoriza al cerrar el grupo de presencia). |
| 7 | `test_no_acepta_terminos` | Sin aceptar los términos se registraba igual: `DID NOT RAISE ErrorInscripcion`. | `inscribir` lanza error si `acepta_terminos` es falso. | No hizo falta. |
| 8 | `test_actividad_inexistente` | "Buceo" se registraba como si existiera: `DID NOT RAISE ErrorInscripcion`. | Nació `reglas.py` con `ACTIVIDADES`; `inscribir` lanza error si la actividad no está en esa lista. | Al cerrar el grupo de presencia: ver fila siguiente. |
| R1 | Refactor del grupo 2 (presencia) | — | — | Se extrajeron `validar_seleccion` (actividad y horario) y `validar_visitante` (nombre, DNI, edad); `inscribir` queda como una lista de pasos. 8 tests en verde. |
| 9 | `test_dni_invalido` (5 casos) | Los 5 DNI mal escritos (con puntos, cortos, largos, con letra, con espacios) se aceptaban: 5 `DID NOT RAISE`. | `validar_visitante` exige que el DNI sea solo dígitos y tenga 7 u 8 caracteres. | No hizo falta. |
| 10 | `test_edad_invalida` (4 casos) | "abc", "-1", "2.5" y "121" se aceptaban como edad: 4 `DID NOT RAISE`. | `validar_visitante` exige que la edad sea solo dígitos (descarta negativos y decimales) y no supere 120. | No hizo falta. |
| 11 | `test_edad_cero_valida` | No hubo Red: pasó de entrada, porque "0" ya cumplía la regla del ciclo 10. Se deja para fijar la decisión de que 0 es válido. | No hizo falta código nuevo. | No hizo falta. |
| 12 | `test_talle_requerido_faltante` | En Palestra, un visitante sin talle se registraba igual: `DID NOT RAISE ErrorInscripcion`. | `Visitante` suma `talle` (vacío por defecto), nace `REQUIEREN_TALLE` en `reglas.py` y se lanza error si la actividad lo pide y falta. | No hizo falta (se espera al resto del grupo). |
| 13 | `test_talle_no_requerido_omitido` | No hubo Red: pasó de entrada, porque el ciclo 12 solo pide talle a las actividades de `REQUIEREN_TALLE`. Cubre la prueba de usuario de la US "sin talle porque no lo requiere (pasa)". | No hizo falta código nuevo. | No hizo falta. |
| 14 | `test_talle_invalido` | En Palestra, el talle "XXXL" se aceptaba: `DID NOT RAISE ErrorInscripcion`. | Nace `TALLES` en `reglas.py`; si la actividad requiere talle, tiene que ser uno de esa lista. | No hizo falta (se espera al resto del grupo). |
| 15 | `test_edad_menor_minimo_palestra` | Un visitante de 11 años se inscribía en Palestra: `DID NOT RAISE ErrorInscripcion`. | Regla escrita a mano y a propósito solo para Palestra (`< 12`): es lo mínimo; el próximo test obliga a generalizarla. | No hizo falta todavía. |
| 16 | `test_edad_menor_minimo_tirolesa` | Un visitante de 7 años se inscribía en Tirolesa: `DID NOT RAISE ErrorInscripcion`. | Se copió la regla de Palestra para Tirolesa (`< 8`): mínimo para pasar, deja la duplicación a la vista. | Ver fila R2. |
| R2 | Refactor edad mínima | — | — | Los dos `if` copiados se reemplazaron por el diccionario `EDAD_MINIMA` en `reglas.py`; las actividades sin límite usan 0 (`.get(actividad, 0)`). 23 tests en verde. |
| 17 | `test_edad_igual_minimo_pasa` | No hubo Red: pasó de entrada, porque la regla usa `<` (12 no es menor que 12). Fija que el mínimo es inclusivo. | No hizo falta código nuevo. | No hizo falta. |
| 18 | `test_safari_sin_limite_edad` | No hubo Red: pasó de entrada, porque Safari no está en `EDAD_MINIMA` y usa 0. | No hizo falta código nuevo. | Ver fila R3. |
| R3 | Refactor del grupo 4 (por actividad) | — | — | Talle y edad mínima pasaron a `validar_reglas_de_actividad`; el doble `actividad in REQUIEREN_TALLE` quedó en un solo `if`. 25 tests en verde. |
| 19 | `test_cantidad_cero` | Una inscripción de 0 personas se registraba: `DID NOT RAISE ErrorInscripcion`. | `inscribir` lanza error si `cantidad` es menor que 1. | No hizo falta. |
| 20 | `test_cantidad_no_coincide_con_visitantes` | Con cantidad 2 y un solo visitante cargado, se registraba igual: `DID NOT RAISE ErrorInscripcion`. | `inscribir` compara `cantidad` con `len(visitantes)` y lanza error si son distintos. | No hizo falta. |
| 21 | `test_actividad_sin_cupo` | Con el turno de Safari lleno (8 de 8), se registraba igual: `DID NOT RAISE ErrorInscripcion`. | Nace `CUPOS` en `reglas.py`; `inscribir` suma las personas ya inscriptas en esa actividad y horario y lanza error si llegan al cupo. El test suma el helper `crear_visitantes`. | No hizo falta todavía. |
| 22 | `test_cantidad_supera_cupo_disponible` | Con 2 lugares libres, una inscripción de 3 personas se registraba: `DID NOT RAISE ErrorInscripcion`. | `inscribir` calcula `disponibles = CUPOS - ocupados` y lanza error si la cantidad lo supera, informando cuántos quedan. | Ver fila R4. |
| R4 | Refactor del cupo | — | — | El conteo pasó a `cupo_disponible(actividad, horario, registro)` y los dos chequeos a `validar_cupo`; `ocupados >= CUPOS` quedó como `disponibles <= 0`. 29 tests en verde. |
| 23 | `test_inscripcion_descuenta_cupo` | No hubo Red: pasó de entrada, porque el refactor R4 ya había creado `cupo_disponible` y el cupo se calcula desde el registro. | No hizo falta código nuevo. | No hizo falta. |
| 24 | `test_turno_fuera_de_rango` (3 casos) | Los turnos de las 8:00, 18:00 y 12:30 se aceptaban: 3 `DID NOT RAISE`. | Nacen `HORA_PRIMER_TURNO` y `HORA_ULTIMO_TURNO`; `inscribir` exige un turno en punto entre las 9 y las 17. | No hizo falta (se espera al resto del grupo). |

## Supuestos

Cosas que no estaban escritas en CLAUDE.md y se resolvieron con la opción más simple.

- "No seleccionar actividad" llega como texto vacío `""` (lo que manda un `<select>` sin elegir).
- "No seleccionar horario" llega como `None`: el dominio recibe el horario como `datetime` y la web pasa `None` si falta.
- Los mensajes de error los redactamos nosotros, siguiendo el texto de los criterios de aceptación.
- Los datos de cada visitante llegan como texto (como vienen del formulario) y el dominio valida su formato.
- Si hay más de un error, se informa solo el primero que se encuentra.
- El talle se compara tal cual, en mayúsculas ("m" no es válido): en la GUI se elige de una lista, así que siempre llega bien escrito.
- Un talle inválido enviado a una actividad que no requiere talle también se ignora (no se valida).
- La cantidad de personas llega como número entero: en la GUI se elige de una lista desplegable y la web la convierte con `int(...)`.
- El cupo no se guarda: se calcula como `CUPOS[actividad]` menos las personas ya inscriptas en ese turno (contadas en `registro`). "Descontar el cupo" es agregar la inscripción al registro.
