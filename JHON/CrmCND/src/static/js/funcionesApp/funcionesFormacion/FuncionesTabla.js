
async function SelectedRow(){
    // Obtén todas las filas de la tabla
    var rows = document.querySelectorAll("#tblpreturnos tr");

    // Agrega un evento clic a cada fila
    rows.forEach(function(row) {
    row.addEventListener("click", function() {
        // Agrega la clase 'selected' a la fila clicada y elimina 'selected' de las filas hermanas
        row.classList.add("selected");
        var siblings = Array.from(row.parentNode.children);
        siblings.forEach(function(sibling) {
        if (sibling !== row) {
            sibling.classList.remove("selected");
        }
        });

        // Obtén el valor de la primera celda de la fila clicada
        var value = row.querySelector("td:first-child").textContent;
        console.log("Valor de la primera celda:", value);
    });
    });
}