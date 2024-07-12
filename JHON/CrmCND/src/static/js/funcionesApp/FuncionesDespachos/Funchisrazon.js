Date.prototype.toDateInputValue = (function() {
    var local = new Date(this);
    local.setMinutes(this.getMinutes() - this.getTimezoneOffset());
    return local.toJSON().slice(0,10);
})


class  HandleTableRazon{
   constructor(idtable){
    this.table =document.getElementById(idtable)
   }

   async #resetTable(){
        this.table.innerHTML=""
   }

   async filldata(ArrayData){
        this.#resetTable()        
        for (var datos of ArrayData) {
            var tr = document.createElement('tr');
            var code = `
                <td>${datos[0]}</td>
                <td>${datos[1]}</td>
                <td>${datos[2]}</td>
                <td>${datos[3]}</td>
                <td>${datos[4]}</td>
                <td>
                    <button class="btn btn-outline-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">Opciones</button>
                    <ul class="dropdown-menu">
                        <li><a class="dropdown-item" href="#" id="btnverraz">Ver</a></li>
                        <li><a class="dropdown-item" href="#" id="btndwnraz">Ver error</a></li>
                        <li><a class="dropdown-item" href="#" id="btnresraz">Reintentar</a></li>
                    </ul>
                </td>
            `;
            tr.innerHTML = code;
            this.table.appendChild(tr);
        }
        

        


   }

   
}



