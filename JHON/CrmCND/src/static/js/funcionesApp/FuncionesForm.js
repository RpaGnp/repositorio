
function FillFormEva(ArrayNotas){
    ArrayCal=Object.values(ArrayNotas)    
    contadorFilas=0        
    for(var dato of ArrayCal){
        contadorCol=0        
        for (var i of dato){                                      
            lista = document.getElementById("tbl_formularioMon");
            var tr = document.createElement("tr");

            var columna0 = document.createElement("th");
            columna0.innerHTML = i['IdItem'];
            columna0.setAttribute("id", "Row" + contadorFilas + "col"+contadorCol);
            columna0.setAttribute("style", "display:none");

            
            lista.appendChild(tr);
            tr.appendChild(columna0);
            contadorCol+=1
        }
        contadorFilas +=1
    }
}
        
        

function GetFilterData(){
    var busqueda = document.getElementById('datatable-search-input');
    var table = document.getElementById("Tbl-HisCasos").tBodies[0];
    texto = busqueda.value.toLowerCase();
    if (texto==""){
      alert("Indique un valor valido!")
      return
    }
      var r=0;
      var Encontrado=false
      while(row = table.rows[r++])
      {
        if ( row.innerText.toLowerCase().indexOf(texto) !== -1 )
          {row.style.display = null;
          Encontrado= true;
        }else{
          row.style.display = 'none';
      }


    
    }
  }


class HandleCardBusqeda{
  constructor(){
    this.busqueda = document.getElementById('datatable-search-input');
    this.table = document.getElementById("Tbl-HisCasos").tBodies[0]; 
  }

  ResetTable(){    
    var r=0;
    var row=""    
    console.log(this.busqueda.value)
    if (this.busqueda.value==""){
      while(row = this.table.rows[r++]){
        row.style.display = null;
      }
    }
  }

  GetFilterData(){    
    var texto = this.busqueda.value.toLowerCase();
    if (texto==""){
      alert("Indique un valor valido!")
      return
    }
      
      var r=0;
      var row="";      
      while(row = this.table.rows[r++]){
        if ( row.innerText.toLowerCase().indexOf(texto) !== -1 )
          { row.style.display = null;          
        }else{
          row.style.display = 'none';
      }
    }
    
  }

  filltablemon(){
    var FecInicio = document.getElementById("Dateinicons").value
    var Fecfin = document.getElementById("Datefincons").value
    if(FecInicio=="" || Fecfin==""){
      alert('ingrese una fecha valida!')
      return
    }
    

  }
}