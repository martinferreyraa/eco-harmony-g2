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

## Supuestos

Cosas que no estaban escritas en CLAUDE.md y se resolvieron con la opción más simple.

- "No seleccionar actividad" llega como texto vacío `""` (lo que manda un `<select>` sin elegir).
- "No seleccionar horario" llega como `None`: el dominio recibe el horario como `datetime` y la web pasa `None` si falta.
- Los mensajes de error los redactamos nosotros, siguiendo el texto de los criterios de aceptación.
- Los datos de cada visitante llegan como texto (como vienen del formulario) y el dominio valida su formato.
- Si hay más de un error, se informa solo el primero que se encuentra.
