// Función para mostrar el modal con la tabla de resultados
function processData(event) {
  event.preventDefault(); // Prevenir el envío del formulario

  // Aquí simulo la respuesta procesada con un ejemplo
  let data = [
    { "Cliente": "Cliente 1", "PH": "PH16", "Cantidad": 5 },
    { "Cliente": "Cliente 2", "PH": "PH3", "Cantidad": 3 }
  ];

  // Crear la tabla HTML
  let table = "<table><tr><th>Cliente</th><th>PH</th><th>Cantidad</th></tr>";

  data.forEach(item => {
    table += `<tr><td>${item.Cliente}</td><td>${item.PH}</td><td>${item.Cantidad}</td></tr>`;
  });

  table += "</table>";

  // Insertar la tabla dentro del modal
  document.getElementById("table-container").innerHTML = table;

  // Mostrar el modal
  document.getElementById("results-modal").style.display = "block";
}

// Función para cerrar el modal
function closeModal() {
  document.getElementById("results-modal").style.display = "none";
}
