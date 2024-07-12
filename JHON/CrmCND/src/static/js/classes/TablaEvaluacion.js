class HandleTabla{    
    constructor(divpadre){
        // crea la tabla dependiendo el dic de datos
        this._divpadre = divpadre;
    }

    LimpiaTabla(){
        let list = document.getElementById(this._divpadre);        
        while (list.hasChildNodes()) {
            list.removeChild(list.firstChild);
          }
    }


    CreadorTabla(values){
        // crea la tabla                           
        var lista = document.getElementById(this._divpadre);
        for (let i = 0; i < values.length; i++){
            let obj = values[i];
            let row = Object.values(obj);                                                        
            //row.splice(5,1 ) //mientras se arregla el procedimiento
            var tr = document.createElement("tr");
            for(var x = 0; x <= 4; x++){                    
                var columna = document.createElement("td");
                columna.innerHTML = row[x];
                columna.setAttribute("id", "Row" + i + "col"+x);
                if(x==0){
                    columna.setAttribute("style", "display:none");
                }
                tr.appendChild(columna)
            }          
            
            var columnaSelects = document.createElement("td");
            var select = document.createElement("select");
            select.setAttribute("class", "form-select");
            select.setAttribute("id", "Row" + i + "col7");
            select.style.width = "200px";
            select.style.top = "50px";
            var ArrayOpciones=["No aplica","Cumple","No cumple"]
            for(var opcion of ArrayOpciones){
                let option = document.createElement("option");                                                    
                option.setAttribute("value", opcion);                          
                option.innerHTML=opcion;
                select.appendChild(option);
            }
            
            if (ArrayOpciones.includes(row[row.length -1 ])){

                select.value= row[row.length -1 ]
            }else{  
                select.value="No aplica"
            }
            
            columnaSelects.appendChild(select);
            tr.appendChild(columnaSelects)
            lista.appendChild(tr);
        }
    }


}