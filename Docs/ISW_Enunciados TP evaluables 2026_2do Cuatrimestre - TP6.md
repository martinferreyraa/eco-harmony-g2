**Universidad Tecnológica Nacional – Facultad Regional Córdoba Cátedra de Ingeniería y Calidad de Software – 2026 Curso: 4K1 - 4K2 - 4K3** 

# **PRÁCTICO 6 -** TDD (Evaluable) 

|**Unidad**:|**Unidad Nro. 4: Aseguramiento de Calidad de Proceso y de Producto**|
|---|---|
|**Consigna:**|Implementar una funcionalidad determinada utilizando el enfoque de_Desarrollo Conducido por Pruebas (TDD)_,<br>en el lenguaje de programación elegido por el grupo, utilizando el enfoque Red-Green-Refactor para construir<br>el código desde las pruebas.|
|**Objetivo:**|Aplicar el enfoque TDD para diseñar y construir software a partir de pruebas automatizadas, poniendo en<br>práctica buenas prácticas de diseño y desarrollo orientado a la calidad desde el inicio.|
|**Propósito:**|Familiarizarse con el ciclo TDD (Red-Green-Refactor), incorporando buenas prácticas de diseño y testing, y<br>fortaleciendo la disciplina del desarrollo guiado por pruebas como base para un código de calidad.|
|**Entradas:**|●<br>Conceptos teóricos sobre el tema desarrollados en clase.<br>●<br>Bibliografía referenciada sobre el tema.<br>●<br>Enunciado del Trabajo Práctico 2: EcoHarmony Park<br>●<br>Definición completa de las User Stories correspondientes al Trabajo Práctico 2 “Requerimientos Ágiles<br>– User Stories y Estimaciones”<br>●<br>Reglas de estilo de código seleccionadas por el grupo para el Trabajo Práctico 2|
|**Salida:**|●<br>Implementación funcional de la User Story asignada<br>●<br>Conjunto de pruebas automatizadas que cubren los distintos casos definidos.<br>●<br>Documento que justifique las decisiones de diseño tomadas.|
|**Instrucciones:**|●<br>Seleccionar una User Story a implementar de entre las siguientes opciones:<br>_○_<br>_Comprar entradas_**(grupos impares)**<br>_○_<br>_Inscribirme a actividad_**(grupos pares)**<br>●<br>Utilizando el lenguaje y documento de estilos de código seleccionado para el Trabajo Práctico 2<br>“Requerimientos Ágiles – User Stories y Estimaciones”, implementar la funcionalidad aplicando el ciclo<br>TDD:<br>○<br>Red: Escribir una prueba que falle.<br>○<br>Green: Implementar el código mínimo para que pase.<br>○<br>Refactor: Mejorar el diseño del código sin romper las pruebas.|



11 

**Universidad Tecnológica Nacional – Facultad Regional Córdoba Cátedra de Ingeniería y Calidad de Software – 2026 Curso: 4K1 - 4K2 - 4K3** 

## **Inscribirme a actividad 5 COMO  visitante  QUIERO inscribirme a una actividad PARA reservar mi lugar en la misma. Criterios de Aceptación:** 

   - Debe requerir seleccionar una actividad del conjunto de actividades de la lista de “Tirolesa”, “Safari”, “Palestra” y “Jardinería”, siempre y cuando tengan cupos disponibles para el horario seleccionado 

   - ● Debe requerir seleccionar el horario dentro de los disponibles 

   - Debe indicar la cantidad de personas que participaran de la actividad 

- Para cada persona que participa, debe ingresar los datos del visitante: nombre, DNI, edad y talla de vestimenta si la actividad lo demanda 

- ● Debe requerir aceptar los términos y condiciones específicos de la actividad en la que participarán. 

- ● Al finalizar la inscripción, se debe enviar un correo electrónico con información de la inscripción realizada. Debe contener un código QR. 

- **Pruebas de usuario:** - Probar inscribirse a una actividad del listado que poseen cupos disponibles, seleccionando un horario, ingresando los datos del visitante (nombre, DNI, edad, talla de la vestimenta si la actividad lo requiere), aceptando los términos y condiciones y recepción del email de confirmación (pasa) 

- - Probar inscribirse a una actividad que no tiene cupo para el horario seleccionado (falla) 

- - Probar inscribirse a una actividad sin ingresar talle de vestimenta porque la actividad no lo requiere (pasa) 

- - Probar inscribirse a una actividad seleccionando un horario en el cual el parque está cerrado o la actividad no está disponible (falla) 

- - Probar inscribirse a una actividad sin aceptar los términos y condiciones de la actividad (falla) 

- - Probar inscribirse a una actividad sin ingresar el talle de la vestimenta requerido por la actividad (falla) 

13 

