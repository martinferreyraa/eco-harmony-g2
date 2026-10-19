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
