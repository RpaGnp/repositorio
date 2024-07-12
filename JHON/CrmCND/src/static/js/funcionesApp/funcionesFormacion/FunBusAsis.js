// clase que implementa la busqueda y organiza la tabla con la inforamcion requerida
    async function SearchName(){
        var input, filtro, tabla, filas, celdas, i, txtValue;
        input = document.getElementById("inpnameaseasi");
        filtro = input.value.toUpperCase();
        tabla = document.getElementById("tblasispret");
        filas = tabla.getElementsByTagName("tr");
        
        for (i = 0; i < filas.length; i++) {
            celdas = filas[i].getElementsByTagName("td")[1]; // La primera celda contiene el nombre

            if (celdas) {
                txtValue = celdas.textContent || celdas.innerText;

                if (txtValue.toUpperCase().indexOf(filtro) > -1) {
                    filas[i].style.display = "";
                } else {
                    filas[i].style.display = "none";
                }
            }
        }
        
        }
    



