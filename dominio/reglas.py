from datetime import timedelta

ACTIVIDADES = ["Tirolesa", "Safari", "Palestra", "Jardinería"]
REQUIEREN_TALLE = ["Palestra", "Tirolesa"]
TALLES = ["XS", "S", "M", "L", "XL", "XXL"]
EDAD_MINIMA = {"Palestra": 12, "Tirolesa": 8}
CUPOS = {"Safari": 8, "Palestra": 12, "Jardinería": 12, "Tirolesa": 10}
HORA_PRIMER_TURNO = 9
HORA_ULTIMO_TURNO = 17
LUNES = 0  # datetime.weekday() devuelve 0 para el lunes
FERIADOS = [(25, 12), (1, 1)]  # (día, mes)
ANTICIPACION_MAXIMA = timedelta(hours=24)
ANTICIPACION_MINIMA = timedelta(minutes=15)

# Textos para revisar por el grupo antes de validarlos con los PO (FAQ #16)
TERMINOS = {
    "Tirolesa": (
        "Es obligatorio usar el arnés y el casco que entrega el parque. "
        "Hay que seguir en todo momento las indicaciones del instructor. "
        "No se puede participar bajo efectos del alcohol, con problemas "
        "cardíacos o en estado de embarazo."
    ),
    "Safari": (
        "Hay que permanecer dentro del vehículo durante todo el recorrido. "
        "No está permitido alimentar, tocar ni llamar a los animales. "
        "Los menores deben ir acompañados por un adulto responsable."
    ),
    "Palestra": (
        "Es obligatorio usar el arnés y el calzado adecuado, y escalar "
        "siempre con la cuerda asegurada por el instructor. Hay que respetar "
        "sus indicaciones y no subir sin autorización. No se puede "
        "participar con lesiones que impidan hacer esfuerzo físico."
    ),
    "Jardinería": (
        "Hay que usar los guantes y las herramientas que entrega el parque "
        "y cuidarlas durante la actividad. Las plantas y semillas no se "
        "pueden retirar del parque. Los menores deben ir acompañados por un "
        "adulto responsable."
    ),
}
