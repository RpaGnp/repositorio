

    var server = "http://10.206.169.143:5000";
    var csrf_token = "{{ csrf_token() }}";    
    var op_num = {'ced':0};     


    $( function() {
        console.log("escribir");
        $( "#inputCedAse").keyup(function() {
            var appdir='/GetDataAseMOn';            
            var n1 = parseInt($("#inputCedAse").val());            
            op_num['ced']=n1;
            
            $.ajax({
                  type: "POST",
                  url:server+appdir,
                  data: op_num,
                  dataType: 'json',
                  headers: {
                    "X-CSRFToken": csrf_token,
                }
                 
            }).done(function(data) { 
                console.log(data);
                $('#inputNomAse').val(data['Nombre']);
                $('#inputProAse').val(data['Proceso']);
                $('#inputEstAse').val(data['Estado']);
                $('#inputCooAse').val(data['cordinador']);
                $('#inputfecIngAse').val(data['fechIngreso']);
                $('#inputForAse').val(data['formador']);
            });
        });

        $("#btn-FromEva").click(function(){
            var appdir='/GetDataFormMon';                         
            var e = document.getElementById("SelProceso");            
            var text = e.options[e.selectedIndex].text;
            var x=document.getElementById("btn-FromEva");
            if(text=='Seleccione...'){
                alert("Seleccione un segmento valido para el asesor seleccionado")
                x.removeAttribute("data-target","#FormCalidadModal");
                x.removeAttribute("data-toggle","modal");
            }else{
                /*data-target="#FormCalidadModal" data-toggle="modal"-->*/               
                x.setAttribute("data-target","#FormCalidadModal");
                x.setAttribute("data-toggle","modal");
                
                let list = document.getElementById("tbl_formularioMon");

                // As long as <ul> has a child node, remove it
                while (list.hasChildNodes()) {  
                    list.removeChild(list.firstChild);
                    }                
                $.ajax({
                    type: "POST",
                    url:server+appdir,
                    data: {'Campaña':text},
                    dataType: 'json',
                    headers: {
                    "X-CSRFToken": csrf_token,}

                }).done(function(data){
                    var values = data['DicDatForm'];                                                            
                    for(let i = 0; i < values.length; i++) {
                        let obj = values[i];
                        let row= Object.values(obj);
                        lista = document.getElementById("tbl_formularioMon");
                        var tr = document.createElement("tr");                       
                        
                        /*console.log('#TblFormcol'+i+'-'+j);*/
                        var columna1 = document.createElement("th")
                        columna1.innerHTML = row[1];
                        columna1.setAttribute('id','Row'+i+'col0');
                        var columna2 = document.createElement("th")
                        columna2.innerHTML = row[2];
                        columna2.setAttribute('id','Row'+i+'col1');
                        var columna3 = document.createElement("th")
                        columna3.innerHTML = row[3];
                        columna3.setAttribute('id','Row'+i+'co20');
                        var columna4 = document.createElement("th")
                        columna4.innerHTML = row[4];
                        columna4.setAttribute('id','Row'+i+'col3');
                        var columna5 = document.createElement("th")
                        columna5.innerHTML = row[5];    
                        columna5.setAttribute('id','Row'+i+'col4');
                        var columna6 = document.createElement("th")
                        columna6.innerHTML = row[6];
                        columna6.setAttribute('id','Row'+i+'col5');
                        var columna7 = document.createElement("th")
                        columna7.innerHTML = row[7];
                        columna7.setAttribute('id','Row'+i+'col6');
                        

                        let select = document.createElement("select");
                        select.setAttribute('class','form-select')
                        select.setAttribute('id','Row'+i+'col7');
                        select.style.width = "200px";
                        select.style.top = "50px";

                        let option1 = document.createElement("option");
                        let  nomclas="SelOpcForMon0"+i;                        
                        option1.setAttribute("class",nomclas);
                        option1.setAttribute("id", nomclas);
                        
                        /*document.getElementById(nomclas).selected = true;*/
                        /*option1.getElementById("SelOpcForMon"+i).selected = true;*/

                        option1.setAttribute("value", "None");
                        let option1Texto = document.createTextNode("Seleccione...");
                        option1.appendChild(option1Texto);
                        select.appendChild(option1);

                        let option2 = document.createElement("option");
                        option2.setAttribute("value", "Cumple");                        
                        let option2Texto = document.createTextNode("cumple");                        
                        option2.appendChild(option2Texto); 
                        select.appendChild(option2);


                        let option3 = document.createElement("option");
                        option3.setAttribute("value", "No_Cumple");                        
                        let option3Texto = document.createTextNode("No cumple");                        
                        option3.appendChild(option3Texto);
                        select.appendChild(option3);

                        document.body.appendChild(select);                        
                        lista.appendChild(tr);
                        tr.appendChild(columna1);
                        tr.appendChild(columna2);
                        tr.appendChild(columna3);
                        tr.appendChild(columna4);
                        tr.appendChild(columna5);
                        tr.appendChild(columna6);
                        tr.appendChild(columna7);
                        tr.appendChild(select);
                    }

                    
                });



            }
        })
        $('#btn-guaForMon').click(function(){            
            var rowsTable = document.getElementById("tbl_formularioMon").rows.length;                        
            var arrayItems  = new Array();
            var arrayCalif = new Array();

            var datos  = [];
            var objeto = {};

            for(let i = 0; i < rowsTable; i++) {                              
                    var Item = document.getElementById('Row'+i+'col5').innerHTML                    
                    var evalItem=document.getElementById('Row'+i+'col7');
                    var OpcSel = evalItem.options[evalItem.selectedIndex].text;                                                           
                    
                    
                    datos.push({ 
                        "Item"    : Item,
                        "Calificacion"  :OpcSel
                    });
                }
            
            objeto.datos = datos;
            DicCal=JSON.stringify(objeto)
            $("#JsonCal").text(JSON.stringify(objeto));            
        })
      });   
    


      


    /*<script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
    <script type=text/javascript>
        $(function() {
        $('input#inputCedAse').on('onkeyup', function(e) {
            e.preventDefault()
            $.getJSON('/background_process_test',
                function(data) {
            //do nothing
            });
            return false;
        });
        });
    </script>-->*/