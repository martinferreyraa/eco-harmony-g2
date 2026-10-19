# Bitácora TDD — Inscribirme a actividad

| # | Test | Red | Green | Refactor |
|---|------|-----|-------|----------|
| 1 | `test_inscripcion_exitosa` | `inscribir` era una función vacía y no registraba nada: `assert 0 == 1`. | Se creó el dataclass `Inscripcion` e `inscribir` la agrega a `registro`. | No hizo falta. |
| 2 | `test_no_seleccionar_actividad` | Con la actividad vacía, `inscribir` la registraba igual: `DID NOT RAISE ErrorInscripcion`. | `inscribir` lanza `ErrorInscripcion("Debe seleccionar una actividad")` si la actividad está vacía. | No hizo falta. |
| 3 | `test_no_seleccionar_horario` | Con el horario en `None`, `inscribir` registraba igual: `DID NOT RAISE ErrorInscripcion`. | `inscribir` lanza `ErrorInscripcion("Debe seleccionar un horario")` si el horario está vacío. | No hizo falta (se espera a que se repita el patrón). |
| 4 | `test_nombre_vacio` | Un visitante sin nombre se registraba igual: `DID NOT RAISE ErrorInscripcion`. | `inscribir` recorre los visitantes y lanza error si alguno no tiene nombre. | No hizo falta. |
| 5 | `test_dni_vacio` | Un visitante sin DNI se registraba igual: `DID NOT RAISE ErrorInscripcion`. | Dentro del mismo recorrido se agregó el chequeo del DNI vacío. | No hizo falta. |
| 6 | `test_edad_vacia` | Un visitante sin edad se registraba igual: `DID NOT RAISE ErrorInscripcion`. | Dentro del mismo recorrido se agregó el chequeo de la edad vacía. | No hizo falta (se refactoriza al cerrar el grupo de presencia). |
