
class handlegesBackog{
    constructor(csrf_token){
        this.csrf_token = csrf_token
        this.tableifo = document.getElementById('tblasigesbacklog').getElementsByTagName("tbody")[0];
        this.tblhisfuturas =document.getElementById('tblhisfuturas').getElementsByTagName("tbody")[0];
        this.tblhisrazones =document.getElementById('tblhisrazones').getElementsByTagName("tbody")[0];
        this.btngetges = document.getElementById('btntakorden')
        this.btnaddtel = document.getElementById('btnadgestel')
        this.btngenges= document.getElementById('btngennotgesase')
        this.btncopy = document.getElementById('btncopnotges')
        this.btnsubmit = document.getElementById('btnsubmittip')
        this.selContacto = document.getElementById('Selgesconaase')
        this.selGestion = document.getElementById('SelGesreaase')
        this.RowTablaNewTel = document.getElementById('rownumtel')
        this.textnoges = document.getElementById('textNotgesase')
        this.jsonNotas={}
        this.contaNumAdd = 1
        this.DicContacto={
            "Contacto":["Adelanto","Agenda cancelada (Solicitud cliente)","Agendada (Primera agenda)",
            "Cancelación OT (Solicitud cliente)","Cierre de escritorio (MTO)","Cliente conveniente","Se respeta agenda","Sin capacidad",
            "Reagendamiento (Razón)","Visita confirmada"
        ],
        "No Contacto":
        ["Marcacion en RR","Se escala a comercial","Se escala a tecnico","Cancelacion Ot (Antiguedad)","Cancelacion ot"],
        "No requiere gestion":["Ya agendada","Cerrada en rr","Cierre softclose","Ya gestionada"]
        }
         
        this.btngetges.addEventListener('click',() =>{
            this.getgestion();
        })

        this.btnaddtel.addEventListener('click',this.AddColTel.bind(this))
        this.selContacto.addEventListener('change',(e)=>{
            this.addoptionconttacto(e)
        })

        this.btngenges.addEventListener('click',()=>{
            this.#addnotasgestion()
        })

        this.btnsubmit.addEventListener('click',(e)=>{
            this.#sendtipasesor()
        })

        this.btncopy.addEventListener('click',()=>{
            this.#CopiarNotasgestion()
        })

        
        document.getElementById('btnverordenes').addEventListener('click',()=>{            
            this.getotsFut()
        });
        
        document.getElementById('btnget5back').addEventListener('click',()=>{            
            this.getotsFut()
        });

    }   

    async getotsFut(){
        this.tblhisfuturas.innerHTML =""
        var code =""
        var Data = await new HandleApis(this.csrf_token,"/ConsultorDatos",{Option:'Getotsfuturas'}).callPromisePost()        
        for( var dato of Data['Arraydatos']){             
            code +=`
            <tr>
                <td>
                    <input class="text-center" type="text" disabled value=${dato[1]}></input>
                </td>
                <td><input class="text-center" type="text" disabled value=${dato[2]}></input></td>
            </tr>
            `
        }
        this.tblhisfuturas.innerHTML=code


    }

    async #CopiarNotasgestion(){
        await navigator.clipboard.writeText(this.textnoges.value)
        alert("Texto copiado!")
    }

    #RecolectorDatos(){
        var JsonNotas={}   
        var Form = document.getElementById('formnotasback')             
        for(var inputs of Form.querySelectorAll('input[type="text"], input[type="tel"],input[type="number"],input[type="time"],textarea,select')){
            if(!inputs.checkValidity()){
                inputs.focus()
                return
            }else{                
                JsonNotas[inputs.getAttribute('aria-label')]=inputs.value
            }
        }
        return JsonNotas
    }

    #getdatatabinfo(){
        var jsontemp= {"IdGestion":document.querySelector('[aria-label="IdGestion"]').innerHTML,"Cuenta":document.querySelector('[aria-label="Cuenta"]').innerHTML,"Orden":document.querySelector('[aria-label="Orden"]').innerHTML,
                        "Asesor":document.querySelector('[aria-label="Asesor"]').value
                        }                
    
        return jsontemp
    }

    #addnotasgestion(){
        this.textnoges.value = ""
        const elemento = document.querySelector('[aria-label="Cuenta"]')
        if (elemento !== null) {
            var jsondatos =this.#getdatatabinfo()
            var Cuenta=jsondatos['Cuenta']
            var Orden=jsondatos['Orden']
            var Asesor=jsondatos['Asesor']
            var Ahora = new Date()
            var FechaActual=`${Ahora.getDate()}/${Ahora.getMonth()+1}/${Ahora.getFullYear()} ${Ahora.getHours()}:${Ahora.getMinutes()}`

            var Notageneral = `GESTION BACK CND OT: ${Orden}\nCuenta: ${Cuenta}\nAsesor: ${Asesor}\nFecha: ${FechaActual}\n`
            this.jsonNotas = this.#RecolectorDatos()
            for (let Key in this.jsonNotas){
                Notageneral += Key+":"+this.jsonNotas[Key]+"\n"
            }
            this.textnoges.value =Notageneral}
        else{            
            showAlertsInfo2({'icon':"error",'Mensaje':'Debe tomar una orden para generar las notas correspondientes!'})
        }        
    }

    async #sendtipasesor(){                
        const resultado = { ...this.#RecolectorDatos(), ...this.#getdatatabinfo() };
        await new HandleApis(this.csrf_token,"/AppDataBase",{"Gestion":'SetTipiasesor',"jsondatos":resultado}).callPromisePost()
        // location.reload()
        document.getElementById('formnotasback').reset()
        this.textnoges.value=""
        await this.getgestion()
    }

    addoptionconttacto(event){
        this.selGestion.innerHTML=""
        var optioncontacto = event.target.value
        var code="<option value=''>..::Seleccione::..</option>"
        for(var opt of this.DicContacto[optioncontacto]){
            code+=`<option value="${opt}">${opt}</option>`
        }
        this.selGestion.innerHTML=code

    }

    #AumContTel(){
        this.contaNumAdd+=1;
    }

    #DisContTel(){
        this.contaNumAdd-=1;
    }

    delrows(button){
        var fila = button.parentNode.parentNode;
        fila.parentNode.removeChild(fila);        
        this.#DisContTel()
    }
    
    #Addfuncdelbtn(){
        this.RowTablaNewTel.addEventListener("click", (e) => {
            if (e.target.classList.contains("delrowtel")) {
                this.delrows(e.target);
            }})
    }

    async FilltableInfo(Arraydatos,detalleorden){
        this.tableifo.innerHTML =""
        var Code=`<tr>
            <td aria-label="IdGestion">${Arraydatos[0]}</td>
            <td aria-label="Tipo orden">${Arraydatos[1]}</td>
            <td aria-label="Cuenta">${Arraydatos[2]}</td>
            <td aria-label="Orden">${Arraydatos[3]}</td>
            <td>${Arraydatos[4]}</td>
            <td>${Arraydatos[5]}</td>
            <td>${Arraydatos[6]}</td>
            <td>${Arraydatos[7]}</td>
        </tr>`   
        this.tableifo.innerHTML=Code

        this.tblhisrazones.innerHTML=""
        var codehisraz=""
        for(var obs of detalleorden){
            codehisraz+=`<tr><td>${obs}</td></tr>`
        }
        this.tblhisrazones.innerHTML=codehisraz

    }   

    async getgestion(){        
        var Data = await new HandleApis(this.csrf_token,"/ConsultorDatos",{Option:'Getgesback'}).callPromisePost()
        if(Data['Arraydatos']==null){
            showAlertsInfo2({'icon':"error",'Mensaje':'NO existe base de gestion cargada, valide con su supervisor!'})
        }else{
            this.FilltableInfo(Data['Arraydatos'],Data['DetalleRazon'])
        }
    }

    async AddColTel(){
        var RowTel = document.createElement("div");
        RowTel.classList.add("row");
        this.RowTablaNewTel.appendChild(RowTel)

        var contTel ="Numero Telefono"+this.contaNumAdd
        var perscon ="Persona_Contesta"+this.contaNumAdd

        const jsonInputs = [{"tipo":"input","options":[],"Atributos":{"class":"form-control","type":"tel","placeholder":contTel,"required":true,"aria-label":contTel}},
        {"tipo":"select","options":['CONTACTO','SE DEJA BUZON','NO PERMITE DEJAR BUZON','TONO AMBULANCIA','TONO CONTINUO','NUMERO EQUIVOCADO'],"Atributos":{"class":"form-select","placeholder":this.contTel,"required":true,"aria-label":"Gestion Numero"+this.contaNumAdd}},
        {"tipo":"input","Atributos":{"class":"form-control","type":"text","placeholder":"Quien contesta","required":true,"aria-label":perscon}},
        {"tipo":"input","Atributos":{"class":"btn btn-danger delrowtel","type":"button","value":"Eliminar","aria-label":contTel}}
        ] 
        
        
        for(let inputs of jsonInputs){
            var tdinptel = document.createElement("div");
            tdinptel.classList.add("col-3", "mb-1");
            var InputTelNue=document.createElement(inputs['tipo']);                
            if(inputs["tipo"]=="select"){
                var optselect = document.createElement("option");
                optselect.textContent = "..::Selecione::.."
                InputTelNue.appendChild(optselect);
                for( let option of inputs["options"]){
                    let opt= document.createElement('option')    
                    opt.value = option
                    InputTelNue.appendChild(opt)
                    opt.textContent = option
                }
            }
            for (let attrib in inputs['Atributos']){
                InputTelNue.setAttribute(attrib, inputs['Atributos'][attrib])
            }            
            

            tdinptel.appendChild(InputTelNue)
            RowTel.appendChild(tdinptel)
            
        }
        this.#AumContTel()
        this.#Addfuncdelbtn()
        return
    }

}