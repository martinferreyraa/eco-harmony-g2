// Avisa si la fecha elegida es un día en que el parque está cerrado.
// Los días cerrados vienen de dominio/reglas.py (la web los pasa al
// template); este script solo los lee. El dominio igual vuelve a validar.

const diasCerrados = JSON.parse(
  document.getElementById("dias-cerrados").textContent
);

function estaCerrado(valor) {
  const [anio, mes, dia] = valor.split("-").map(Number);
  const fecha = new Date(anio, mes - 1, dia);
  // JavaScript cuenta el domingo como 0; Python cuenta el lunes como 0
  const diaComoEnPython = (fecha.getDay() + 6) % 7;
  if (diaComoEnPython === diasCerrados.lunes) {
    return true;
  }
  for (const [diaFeriado, mesFeriado] of diasCerrados.feriados) {
    if (dia === diaFeriado && mes === mesFeriado) {
      return true;
    }
  }
  return false;
}

function revisarFecha(campo) {
  const aviso = document.querySelector("[data-aviso-fecha]");
  let mensaje = "";
  if (campo.value && estaCerrado(campo.value)) {
    mensaje = "El parque está cerrado ese día. Elegí otra fecha.";
  }
  campo.setCustomValidity(mensaje);
  aviso.textContent = mensaje;
  aviso.hidden = mensaje === "";
  if (mensaje) {
    // FAQ #2: el día cerrado no queda seleccionado
    campo.value = "";
  }
}

for (const campo of document.querySelectorAll("[data-dias-cerrados]")) {
  campo.addEventListener("change", () => revisarFecha(campo));
  revisarFecha(campo);
}
