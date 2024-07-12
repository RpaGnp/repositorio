

class handleTableAsesores{
    constructor(csrf_token,idtable){
        this.table = document.getElementById(idtable)        
        this.csrf_token = csrf_token
    }
    async #resetTable(){
        this.table.innerHTML=""
    }

    async ConstruirHeadTable(ArrayEncabezados){        
        var Trcode = `<thead><tr>`        
        for(var td of ArrayEncabezados){
            var tdcode =`<th>${td}</th>`
            Trcode += tdcode
        }
        Trcode +=`</tr></thead>`        
        this.table.innerHTML = Trcode

    }

    async ConstruirBody(Data){
        var BodyTabla= this.table.appendChild(document.createElement("tbody"))
    }

   
}


class handleformRemocion{
    constructor(csrf_token,idnumerario){
        this.csrf_token=csrf_token
        this.idnumerario =idnumerario
        this.BodyTableAsesor=document.getElementById('tdyinfasesor')
        // funciones externas
        this.ConsultorApis = new ConsultorApis(csrf_token)
        
    }
    async #filldataasesor(arrayDatos){
        this.BodyTableAsesor.innerHTML=""
        var dato = arrayDatos['DicDatos']        
        if(dato.length!=0){
            this.BodyTableAsesor.innerHTML=`<tr style="background-color:#1CC88A;color:white"><td>${dato[1]}</td><td>${dato[3]}</td><td>${dato[6]}</td><td>${dato[7]}</td></tr>`  
        }else{
            alert("Usuario no existe!")
        }
        
        
    }

    #reserform(){
        document.getElementById('FormRemocion').reset()
        this.BodyTableAsesor.innerHTML=""
    }   

    async BuscarAsesor(){
        var IdAsesor = document.getElementById("IdAsesor").value        
        if(IdAsesor!=""){
            const Data = await new HandleApis(this.csrf_token,"/ConsultorDatos",{'Option':'getdatasecon','cedase':IdAsesor}).callPromisePost()
            await this.#filldataasesor(Data)
        }
        else{
            alert("Ingrese un dato valido!")

        }

    }

    async SendFormRem(){
        var IdAsesor=document.getElementById('IdAsesor').value
        var NotAsesor=document.getElementById('inpnotasesor').value
        var segasesor = document.getElementById('SelSegmento').value
        var tableitemsafe = document.getElementById('tblbdyiteseg')        

        var jsonItemsAfe ={}
        var arraytemp= []
        for (var i = 0, row; row = tableitemsafe.rows[i]; i++) {     
            var resItem = row.cells[2].querySelector('input[type="checkbox"]').checked
            if (resItem== true){    
                arraytemp.push({"IdItem":row.cells[0].innerText,"NumItem":row.cells[1].innerText,"ResGes":resItem})
            }else{
                continue
            }
        }
        jsonItemsAfe={"ArrayItems":arraytemp}         
        var obsremo = document.getElementById('Inpobsrem').value

        const Data = await this.ConsultorApis.callpost("/AppDataBase",
            {'Gestion':'InsNueRem',"Numerario":this.idnumerario,'cedase':IdAsesor,'NotAse':NotAsesor,
            'SegAsesor':segasesor,"ItemsAsesor":jsonItemsAfe,
            "ObsRemocion":obsremo})
        await showAlertsInfo2({'icon':"success",'Mensaje':'Remocion N° '+Data['Radicado']+' creda con exito!, puede consultarala en la vista historial'})
        this.#reserform()
    }


    async getitems(segmento){        
        /*trae los datos por segmento*/        
        const tablaItems= document.getElementById('tblbdyiteseg')
        tablaItems.innerHTML=""
        const data =await this.ConsultorApis.callpost("/ConsultorDatos",
            {'Option':'getitemsbyseg','Campaña':segmento}
            )        
        var tempCode =``
        data['DicDatos'].forEach(element => {
            tempCode+=`<tr>
                <td>${element[0]}</td><td>${element[1]}</td>
                <td class="form-check">                    
                    <input class="form-check-input ms-2" type="checkbox" id="checkbox${element[0]}">
                    <label class="form-check-label ms-4" for="checkbox${element[0]}">No cumple</label>
    
                </td>
            </tr>`
        });
        tablaItems.innerHTML=tempCode
    }
    

}

class HandleFiles {
    constructor(csrf_token){
        this.csrf_token =csrf_token
        // funciones externas
        this.ConsultorApis = new ConsultorApis(csrf_token)
        
    }
    obtenerBlob(FileId) {
        //this.ConsultorApis.callpost("/ConsultorDatos",{"Option":'DwPretFile',"PretId":FileId})            
        const options = {
            method: "POST",
            headers: {
                'Accept': 'application/json, text/plain, */*',
                'Content-Type': 'application/json',
                "X-CSRFToken": this.csrf_token,
            },
            body: JSON.stringify({Option:'DwPretFile',PretId:FileId}),        
            };
        fetch("/ConsultorDatos",options)
        .then(response => response.blob())
            .then(blob => {
                var url = window.URL.createObjectURL(blob);
                var a = document.createElement('a');
                window.open(url, '_blank');

            })
    }
}

///historial de remociones, zona peligrosa para manzanas
class handletablahistorico{
    constructor(csrf_token,idtable){
        this.idRemocion = document.getElementById('idremocion')
        this.table=document.getElementById(idtable)
        this.csrf_token = csrf_token
        this.tableinfoasesor = document.getElementById('tblbdyasesor')
        this.tableinfocalidad = document.getElementById('tblbdycalidad')
        this.tableinfosegcal = document.getElementById('tblbdysegcal')
        this.tableinfoform = document.getElementById('tblbdyeva')
        this.tableinfope =document.getElementById("tblbdyoperacion")
        this.selmatestudio = document.getElementById('Selmatestudio')
        this.selidmonitoreo =document.getElementById('SelIdMon')
        this.txtobssupervisor = document.getElementById('txtcomsuprem') 
        /// botones
        this.btnasimat = document.getElementById('btnasimatest')
        this.btverpdf = ""
        this.btpreeva = ""
        this.btnasimoncal = document.getElementById('btnasimonrem')
        this.btnguaobssup = document.getElementById('btnguacomsuprem')
        // funciones externas
        this.ConsultorApis = new ConsultorApis(csrf_token)        
    }

    async #desbtn(Boton){                   
        var button = document.getElementById(Boton)        
        button.disabled = true;
    }

    async #actbtn(Boton){        
        var button =document.getElementById(Boton)
        button.disabled = false;
    }

    async delrow(element){
        var confirmacion = await alertConfirmacion({'titulo':"Eliminacion remocion!",
        "mensaje":"Desea eleminiar de forma permanente la remocion "+element+"?","icono":"question"})        
        if (confirmacion.isConfirmed){
            const Data = await new HandleApis(this.csrf_token,"/AppDataBase",
            {'Gestion':'DelRem',"Numerario":element}).callPromisePost()        
            location.reload()
        }else{
            return}
    }

    async getdataremocion(idremocion){
        this.idRemocion.value = idremocion;        
        const Data = await this.ConsultorApis.callpost("/ConsultorDatos",
            {'Option':'GetdatRem',"Numerario":idremocion})        

        var dato = Data['DataAsesor']
        var codetemp =`<tr><td hidden id="idaserem">${dato[0]}</td><td>${dato[1]}</td><td>${dato[2]}</td><td>${dato[3]}</td><td>${dato[4]}</td><td>${dato[5]}</td><td>${dato[6]}</td></tr>`        
        this.tableinfoasesor.innerHTML=codetemp
        var codetemp =`<tr><td>${dato[7]}</td><td>${dato[8]}</td><td>${dato[9]}</td><td>${dato[10]}</tr>`
        this.tableinfocalidad.innerHTML=codetemp
        
        tempcode=""
        JSON.parse(dato[31]).ArrayItems.forEach( async (item)=> {
            tempcode += `<tr>
                <td>${item['NumItem']}</td><td>No cumple</td>
            </tr>`

        })
        document.getElementById('tblbdyitemcal').innerHTML=tempcode

        // selects de preturno         
        if(Data['DataMaterial'].length==0){
            var temcode=`<option value="${dato[11]}">${dato[12]}</option>`
            this.selmatestudio.innerHTML=temcode
            this.selmatestudio.value=dato[11]
            this.selmatestudio.setAttribute("disabled",true)                        

        }else{
            var temcode='<option value="">..::Selecione::..</option><option value="0">No aplica</option>'

            for(var Opt of Data['DataMaterial']){                
                temcode += `<option value="${Opt[0]}">${Opt[1]}</option>`
            }
            this.selmatestudio.innerHTML=temcode
            this.selmatestudio.removeAttribute("disabled")
        }
        //data formacion
        document.getElementById('lnkmatstudio').innerHTML= `<input type="button" class="btn btn-outline-primary" id="btndwpret" aria-label='${dato[11]}' value="Ver">` 
        this.btverpdf = document.getElementById('btndwpret')
        document.getElementById('btndwpret').addEventListener('click',(e)=>{
            const ariaLabel = e.target.getAttribute('aria-label');                    
            handleFiles.obtenerBlob(ariaLabel)
        })
        
        this.tableinfoform.innerHTML=`
        <td><a class="btn btn-outline-success" href="/Evaluaciones/${dato[11]}/${usuNumerario}" id="btnevaluacion">Evaluacion</a></td>
        <td>${dato[14]}</td>        <td>${dato[15]}</td>        <td>${dato[16]}</td>
        <td>${dato[17]}</td>        <td>${dato[18]}</td>        <td>${dato[19]}</td>
        <td>${dato[20]}</td>        
        `
        this.btpreeva = document.getElementById('btnevaluacion')
        // data calidad             
        if(Data["DataMonAsesor"].length == 0){
            var tempcode='<option value="">..::Selecione::..</option><option value="0">No aplica</option>'
            var tempcode = `<option value=${dato[21]}>${dato[21]}</option>`
            this.selidmonitoreo.innerHTML=tempcode
            this.selidmonitoreo.value=dato[21]
            this.selidmonitoreo.setAttribute("disabled",true)
        }else{
            var tempcode='<option value="">..::Selecione::..</option><option value="0">No aplica</option>'
            for(var Opt of Data['DataMonAsesor']){                
                tempcode += `<option value="${Opt[0]}">${Opt[0]}</option>`
            }
            this.selidmonitoreo.innerHTML=tempcode
            this.selidmonitoreo.removeAttribute("disabled")
            
        }
        // llenar los datos de seguimiento calidad
        this.tableinfosegcal.innerHTML=`<tr>
            <td>${dato[22]}</td>
            <td>${dato[23]}</td>
            <td>${dato[24]}</td>
            <td>${dato[25]}</td>
            <td>${dato[26]}</td>
        </tr>`
        this.tableinfope.innerHTML=`<tr>
        <td>${dato[27]}</td>
        <td>${dato[28]}</td>
        <td>${dato[29]}</td>
        </tr>`        
        this.txtobssupervisor.value=dato[30]
        

        // interacion botones
        for(var key in Data['DicBotones']){
            switch (Data['DicBotones'][key]){
                case 0:
                    await this.#desbtn(key)
                    break
                default:
                    await this.#actbtn(key)
                    break
            }
        }

    }

    async setmatremo(){
        var idRemocion=document.getElementById('idremocion').value
        var Idmatremo = document.getElementById('Selmatestudio').value
        const Data = await new HandleApis(this.csrf_token,"/AppDataBase",
            {'Gestion':'SetMatRemocion','idremocion':idRemocion,'idmatrem':Idmatremo}).callPromisePost() 
        /* document.getElementById("btnasimatest").setAttribute("disabled",true) */
        this.getdataremocion(idRemocion)
    }

    async setmonremo(){
        var IdMon =document.getElementById('SelIdMon').value
        var IdRem = this.idRemocion.value
        console.log(IdMon)
        console.log(IdRem)
        await this.ConsultorApis.callpost("/AppDataBase",
            {'Gestion':'SetMonRemocion','idremocion':IdRem,'idmonrem':IdMon}
            )
        this.getdataremocion(IdRem)
        await showAlertsInfo2({"Mensaje":"Monitoreo "+IdMon+" asignado con exito a la remocion "+IdRem,"icon":"success"})
        /* document.getElementById("btnasimonrem").setAttribute("disabled",true)*/
    }

    async setobssuprem(){
        var comp = this.txtobssupervisor.value
        if (comp===""){
            await showAlertsInfo2({"Mensaje":"Ingrese las observaciones pertinentes a la remocion","icon":"question"})
        }else{
            await this.ConsultorApis.callpost("/AppDataBase",
            {'Gestion':'SetObsRemocion','idremocion':this.idRemocion.value,'obsergestion':comp}
            )
            await showAlertsInfo2({"Mensaje":"Observaciones de seguimiento por parte de la operacion guardadas cn exito","icon":"success"})
            this.txtobssupervisor.setAttribute("disable",true)
        }

    }

}




