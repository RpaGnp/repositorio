function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function HeaderFetch(csrf_token,JsonDatos){    
    const options = {
        method: "POST",
        headers: {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            "X-CSRFToken": csrf_token,
        },
        body: JSON.stringify(JsonDatos),        
        };
    return options
}

function FillData(ArrayValuesJson,ArrayidTag){
    contador=0    
    for(var idtag of ArrayidTag){
        document.getElementById(idtag).value = ArrayValuesJson[contador];  
        contador+=1
      }
    delete contador
}   


async function FillDataSeg(csrf_token, Segmento,arraySelects){
    if (Segmento==""){return}
    
    const  dataOpt= await callPromise(csrf_token,"/SelectInteractivos",{Proceso:Segmento}    
    )    
      const selTipoOrden=document.getElementById(arraySelects[0])
      while (selTipoOrden.options.length > 0) {
            selTipoOrden.remove(0);
        }
      
      for(var i of [dataOpt['TIPOORDEN']][0]){
          let opt=document.createElement('option')
          opt.value=i
          opt.innerHTML=i
          selTipoOrden.appendChild(opt)
      }
      
      const selRazon=document.getElementById(arraySelects[1])
      while (selRazon.options.length > 0) {
        selRazon.remove(0);
    }

      for(var i of [dataOpt['RAZONES']][0]){
        let opt=document.createElement('option')
        opt.value=i
        opt.innerHTML=i
        selRazon.appendChild(opt)      
      }
}

function GetItemCal(){
      var rowsTable = document.getElementById("tbl_formularioMon").rows.length;      
      var datos = [];
      var json = {};

      for (let i = 0; i < rowsTable; i++) {
        var idItemcali = document.getElementById("Row" + i + "col0").innerHTML;
        var Itemcali = document.getElementById("Row" + i + "col3").innerHTML;
        var Pesocali = document.getElementById("Row" + i + "col4").innerHTML;
        var evalItem = document.getElementById("SelRow" + i + "col6").value;

        datos.push({
        IdItem: idItemcali,
        Item: Itemcali,
        Precicion: Pesocali,
        Calificacion: evalItem})

      } // end for
      return datos
    
    }



    function GetItemCalHp(){
        var rowsTable = document.getElementById("tbl_formularioMon").rows.length;      
        var datos = [];
        var json = {};
  
        for (let i = 0; i < rowsTable; i++) {
            var idItem = document.getElementById("Row" + i + "col0").innerHTML;          
            var Item = document.getElementById("Row" + i + "col1").innerHTML; 
            var evalItem = document.getElementById("Row" + i + "col7");
            var OpcSel = evalItem.options[evalItem.selectedIndex].text;
  
            var OpcSel = evalItem.options[evalItem.selectedIndex].text;
          if (OpcSel == "Seleccione...") {
            document.getElementById("SelRow" + i + "col7").focus();
            var evalItem = document.getElementById("Row26col7")
            
            return;
          } else {
              datos.push({IdItem: idItem,Tipologia:Tipo,Item: Item,Peso: Peso,Calificacion: OpcSel})            
          }
        } // end for
  
        
        
        return datos
      
      }


function makeJson(arrayKeys,arrayValues){        
    json={}
    contador=0
    for(var i of arrayKeys){
        json[i] =arrayValues[contador] ;
        contador+=1
    }
    return json
}



async function callPromise(csrf_token,api,jsonOptions){    
    options=HeaderFetch(csrf_token,jsonOptions);        
    await fetch(api,options).then(response => response.text()).then(data => {        
        list_items  = JSON.parse(data);                                            
    }).catch((error) => {
        console.log('Error:', error);}
    )
    return list_items;
    }



async function recolectorDatos(idasecal){
    datos=[]
    //datos de los inputs                       
    for (let dato of ["inputCedAse","inpSede","inputFechMon","inputCueAse","inputOrdAse","inpFechAge","inputidlla","inpuObseMon"]) {
      datos.push(document.getElementById(dato).value);
    };
    //datos de los selects
    for (let selector of ["SelAreaMon","SelAuditor","SeltipGes","SeltipMon1","SelTipOrd","SelRazonMon"]){    
      var evalItem = document.getElementById(selector);
      var OpcSel = evalItem.options[evalItem.selectedIndex].text;
      if (OpcSel == "Seleccione...") {
        document.getElementById(selector).focus();
        datos=[]
        return;
      }else{
          datos.push(OpcSel);
      }
    }
    datos.push("N/A");
    //valores label calificacion
    for (let dato of [
      "lbl_NotMonTotal",
      "lbl_NotMonec",
      "lbl_NotMonenc"
    ]) {
      datos.push(document.getElementById(dato).innerHTML);
    }
    datos.push("N/A")
    //var IdAuditor=${current_user.id}
    datos.push(document.getElementById("inputIteAfe").value);
    
    datos=[datos[0],idasecal ,datos[1],datos[8],datos[9],datos[10],datos[11],datos[2],datos[3],datos[4],datos[5],datos[12],datos[6],datos[13],datos[14],datos[7],datos[15],datos[16],datos[17],datos[18],datos[19]];
    const jsonString = JSON.stringify(Object.assign({}, datos));
    return jsonString
  }


async function CalNotMon(){        
    var rowsTable = document.getElementById("tbl_formularioMon").rows.length;      
    var datos = [];
    // var objeto = {};

    if(document.getElementById("SeltipGes").value=="HHPP"){
      for (let i = 0; i < rowsTable; i++) {
        var idItem = document.getElementById("Row" + i + "col0").innerHTML;          
        var Item = document.getElementById("Row" + i + "col1").innerHTML; 
        var evalItem = document.getElementById("Row" + i + "col7");
        var OpcSel = evalItem.value;                            
        datos.push({
          IdItem: idItem,            
          Item: Item,                        
          Calificacion: OpcSel,
        });        
      }          
      // objeto.datos = datos;
      // DicCal = JSON.stringify(objeto);      
      ArrayCal=JSON.stringify(datos)            
      document.getElementById("inputIteAfe").value = ArrayCal;                      
      
      
      var  data= await callPromise(csrf_token,"/CalcNotaMon",{ Segmento:"HHPP", DatoForm: ArrayCal })                  

    }else{
      for (let i = 0; i < rowsTable; i++) {        
        var idItem = document.getElementById("Row" + i + "col0").innerHTML;
        var Item = document.getElementById("Row" + i + "col3").innerHTML;
        var Peso = document.getElementById("Row" + i + "col4").innerHTML;        
        var evalItem = document.getElementById("Row" + i + "col7");
        var OpcSel = evalItem.value;                 
        datos.push({
          IdItem: idItem,
          Item: Item,
          Peso: Peso,
          Calificacion: OpcSel,
        });        
      }
      //objeto.datos = datos;
      //DicCal = JSON.stringify(objeto);
      //document.getElementById("inputIteAfe").value = JSON.stringify(objeto);
      ArrayCal=JSON.stringify(datos)            
      document.getElementById("inputIteAfe").value = ArrayCal;                
      
      var  data= await callPromise(csrf_token,"/CalcNotaMon",{ Segmento:"HOGAR",DatoForm: ArrayCal })

    }    
    if(parseInt(data["NotaTotal"])==100){
      $("#lbl_NotMonTotal").css("background-color","#4ed2ad")}
    else if(parseInt(data["NotaTotal"]>=80 & parseInt(data["NotaTotal"])<=89)){
      $("#lbl_NotMonTotal").css("background-color","#ff6d2a")
    }
    else if(parseInt(data["NotaTotal"])<=79){
      $("#lbl_NotMonTotal").css("background-color","#d1052a");
    }
    $("#lbl_NotMonTotal").html(data["NotaTotal"]);
    $("#lbl_NotMonec").html(data["TotalNoCritico"]);
    $("#lbl_NotMonenc").html(data["TotalCrit"]);
    await showAlertsInfo(
      {"icon":"success","Mensaje":"Resultado de la calificacion: " +data["NotaTotal"] +"!"}
      )
  };

  // calcular una nota promedio del asesor
    async function Cacnotmes(arraydatos){
      var totalNotas=arraydatos.length
      var Contapr =0
      arraydatos.forEach((element) => {
      if (element[5]>=90) {
        Contapr+=1
      }
      });

      return ((Contapr/totalNotas)*100).toFixed(2)

    }

