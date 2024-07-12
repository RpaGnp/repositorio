class handleFormEva{
    constructor(){
        this._ArrayidTag=['inpSede',"SelAreaMon","SelAuditor","SeltipGes","SeltipMon1","inputFechMon",
        "inputCedAse","inputNomAse","inputProAse","inputCooAse","inputForAse","inputfecIngAse",
        "inputCueAse","inputOrdAse","inpFechAge","SelTipOrd","inputidlla","SelRazonMon",
        "selHorReg","inpuObseMon"];
        this._selTipOrden="SelTipOrd"
        this._selRazon="SelRazonMon"
    }

    

    async FillDataForm(ArrayValuesJson){
        let contador=0    
        for(var idtag of this._ArrayidTag){                    
            document.getElementById(idtag).value = ArrayValuesJson[contador];  
            contador+=1
          };
        
    }   
    

    async FillDataFormSeg(dataOpt){        
        const selTipoOrden=document.getElementById(this._selTipOrden)
        while (selTipoOrden.options.length > 0) {
                selTipoOrden.remove(0);
            }
      
      for(var i of [dataOpt['TIPOORDEN']][0]){
          let opt=document.createElement('option')
          opt.value=i
          opt.innerHTML=i
          selTipoOrden.appendChild(opt)
      }
      
      const selRazon=document.getElementById(this._selRazon)
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

    async FillTablaNotas(data){
      var ArrayNotas=[21,22,23,24]
      var contador=0
      for(var i of ['lbl_NotMonTotal','lbl_NotMonec','lbl_NotMonenc']){
          document.getElementById(i).innerHTML = data['DataForm'][ArrayNotas[contador]]
          contador+=1
      }
    }
  
  async FillRazones(JsonDatos){    
    var Data=   JsonDatos['DataForm']    
    document.getElementById("SelTipOrd").value = Data[15]
    document.getElementById("SelRazonMon").value = Data[17]
    return "Realizado ok"
  }

  async RecolectorForm(idasecal){
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
    datos=[datos[0],idasecal ,datos[1],datos[8],datos[9],datos[10],datos[11],datos[2],datos[3],datos[4],datos[5],datos[12],
    datos[6],datos[13],datos[14],datos[7],datos[15],datos[16],datos[17],datos[18],datos[19]];
    const jsonString = JSON.stringify(Object.assign({}, datos));
    return jsonString

  }

  
}