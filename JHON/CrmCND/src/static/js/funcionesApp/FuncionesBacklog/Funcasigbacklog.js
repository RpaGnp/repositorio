function toggleCell(button) {
    var Id = button.getAttribute('name');
    var extraRow = document.getElementById("RowHide"+Id)
    if (extraRow.style.display === "none") {
        extraRow.style.display = "table-row";
        button.textContent = "-";
    } else {
        extraRow.style.display = "none";
        button.textContent = "+";
    }
}



class handletablahistorico{
    constructor(csrf_token){
        this.csrf_token = csrf_token  
        this.btnfill = document.getElementById('btnfilgesback')
        this.tablehis = document.getElementById('tblhisgesback').getElementsByTagName('tbody')[0]
        this.Callapi = new ConsultorApis(this.csrf_token)  
        this.tblcanbase = document.getElementById('tbldesbaseback').getElementsByTagName('tbody')[0]
        this.jsonestbases={}
        this.mdltbldetgesase = document.getElementById('tbldetgesase').getElementsByTagName('tbody')[0]
        this.selebasesmetback = document.getElementById('Selbasbackmet')

        document.getElementById('btndesbaseback').addEventListener('click',() =>{
            this.#filltablacanbase()
        })



        document.getElementById('btndwgesase').addEventListener('click',() =>{
            this.#gendwgestion()
        })

        document.getElementById('btnmetgesback').addEventListener('click',() =>{
            this.#showmetgestion()
        })

        document.getElementById('btnupdmet').addEventListener('click',() =>{
            this.#showmetgestion()
        });
        this.selebasesmetback.addEventListener('change',(e) =>{
            this.#getmetgesbybase(e)
        });

        document.getElementById("btnupdhisraz").addEventListener('click',(e) =>{
            this.#updbaseconmongo()
        });

        this.#asigfuntbtn(this.csrf_token)
    }
    //================================funciones de la aplicacion================================
    async #updbaseconmongo(){
        document.getElementById('lblestupbasemongo').innerHTML="Generando actualizacion de base de datos desde shateir point"
        var data = await new ConsultorApis(this.csrf_token).callpost("/AppDataBase",{"Gestion":"Updbasemongo"})
        if (data['Res']==0){

            alert("Carga fallida, favor valide con su administrador de sistema!")
        }
        document.getElementById('lblestupbasemongo').innerHTML=data['Res'] }


    async #getmetgesbybase(e){
        var idbase= e.target.value
        console.log(idbase)
        if(idbase=="Todas"){
            let inpfechfill = document.getElementById('inpfecgesback').value
            var Data = await new ConsultorApis(this.csrf_token).callpost("/ConsultorDatos",{"Option":"Getmetrisback","Fecha":inpfechfill})
            console.log(Data)
        }else{
            var Data = await new ConsultorApis(this.csrf_token).callpost("/ConsultorDatos",{"Option":"Getmetbybase","IdBase":idbase})
        }
        const table = document.getElementById("tblmetgesback").getElementsByTagName('tbody')[0]
        table.innerHTML =""
        var code =""
        Data['Arraydatos'].forEach(element => {
            code+=`<tr>
                <td>${element[0]}</td>
                <td>${element[1]}</td>
                <td>${element[2]}</td>
                <td>${element[3]}</td>
                <td>${element[4]}</td>
                <td>${Math.trunc((element[4]/element[3])*100)}%</td>
                <td>${Math.trunc((element[3]/element[1])*100)}%</td>
            </tr>`
        });
        table.innerHTML = code
    }

    async #getbaseactdia(fecha){
        const Data = await new ConsultorApis(this.csrf_token).callpost("/ConsultorDatos",{"Option":"Getbasebackdia","Fecha":fecha})
        return Data['Arraydatos']
    }
    async #showmetgestion(){
        const inpfechfill = document.getElementById('inpfecgesback').value
        if(inpfechfill===""){
            alert("Por favor escoja una fecha valida")
            return false
        }
        // trae los datos de las bases activas
        var basesback = await this.#getbaseactdia(inpfechfill)
        this.selebasesmetback.innerHTML=""
        var code ="<option value=''>..::Seleccione::..</option><option value='Todas'>Todas</option>"

        basesback.forEach(element =>{
            code += `<option value='${element[0]}'>${element[1]}</option>`
        })
        this.selebasesmetback.innerHTML=code



        const Data = await new ConsultorApis(this.csrf_token).callpost("/ConsultorDatos",{"Option":"Getmetrisback","Fecha":inpfechfill})
        const table = document.getElementById("tblmetgesback").getElementsByTagName('tbody')[0]
        table.innerHTML =""
        var code =""
        Data['Arraydatos'].forEach(element => {
            code+=`<tr>
                <td>${element[0]}</td>
                <td>${element[1]}</td>
                <td>${element[2]}</td>
                <td>${element[3]}</td>
                <td>${element[4]}</td>
                <td>${Math.trunc((element[4]/element[3])*100)}%</td>
                <td>${Math.trunc((element[3]/element[1])*100)}%</td>
            </tr>`
        });
        table.innerHTML = code
    }

    async #gendwgestion(){
        const inpfechfill = document.getElementById('inpfecgesback').value
        if(inpfechfill===""){
            alert("Por favor escoja una fecha valida")
            return false
        }
        await new ConsultorApis(this.csrf_token).callFile("/ConsultorDatos",{"Option":"Getdwgesback","Fecha":inpfechfill})

    }

    async #aplicanbases(){        
        const filas = this.tblcanbase.getElementsByTagName('tr');        
        for(let i = 0; i < filas.length; i++){
                // comparar el element con el original y aplicar cambios a los cambios del element
                var idRow = parseInt(filas[i].querySelector('[arial-label]').innerHTML);   
                var estadoRow = filas[i].querySelector("[type='checkbox']").checked;                
                if(this.jsonestbases[idRow] != estadoRow){                    
                    await new HandleApis(this.csrf_token,"/AppDataBase",{Gestion:'Desbasbacks',idbase:idRow}).callPromisePost()    
                }
            
        }   
        alert("Cambios aplicados correctamente!")
        
    }

    async #fillmdldetges(Cuenta,Orden,Asesor,arraydatos){
        document.getElementById('cldCuenta').innerHTML = Cuenta
        document.getElementById('cldOrden').innerHTML = Orden
        document.getElementById('cldAsesor').innerHTML= Asesor        
        var arrayceld =['cldges','cldfecges','cldhorges','cldcont','cldredcont','cldobs']
        for (let i=0; i<arrayceld.length; i++) {
            console.log(arrayceld[i])
            console.log(arraydatos[i])
            document.getElementById(arrayceld[i]).innerHTML = arraydatos[i]
        }        
    }

    async #asigfundestab(CSRFToken){
        const self = this;
        $('#tbldesbaseback').on('click', '.btn-outline-success',async function (e){
            let currentRow=$(this).closest("tr");
            let Idbase=currentRow.find("td:eq(0)").text();
            let EstadoBase=currentRow.find("td:eq(2)").find("input[type='checkbox']").prop("checked");;
            let MotivoDesBase=currentRow.find("td:eq(6)").find("select").val();

            let ArrayCheckAsesor = currentRow.next("tr").find("[type='checkbox']");
            let jsonestadoasesor = {};
            ArrayCheckAsesor.each((index, element)=>{
                let id = $(element).attr("id");
                let isChecked = $(element).prop("checked");
                jsonestadoasesor[id] = isChecked;
            });

            await new HandleApis(CSRFToken,"/AppDataBase",{"Gestion":"Updestbaseback",
               "idbase": Idbase,"EstadoBase":EstadoBase,"MotivoBase":MotivoDesBase,
               "JsonAsesores":jsonestadoasesor}).callPromisePost()

            alert("Cambios aplicados con exito!")
        })
    }

    async #asigfuntbtn(CSRFToken){
        const self = this;
        $('#tblhisgesback').on('click', '.btndetgesase',async function (e){
            var currentRow=$(this).closest("tr");
        
            var Idrow=currentRow.find("td:eq(0)").text();
            var Cuenta=currentRow.find("td:eq(2)").text();
            var Orden=currentRow.find("td:eq(3)").text();
            var Asesor=currentRow.find("td:eq(7)").text();
            
            if (parseInt(currentRow.find("td:eq(8)").text())==1){
                // trae la info de la orden
                var Data = await new HandleApis(CSRFToken,"/GetdataAPI",{Req:"Getdetgesord",norden:Idrow}).callPromisePost()    
                await self.#fillmdldetges(Cuenta,Orden,Asesor,Data['Arraydatos'])
            }else{
                await self.#fillmdldetges(Cuenta,Orden,Asesor,["--","--","--","--","--","--"])
            }
            
        })  
    }

    async filltable(ArrayDatos) {
        if(ArrayDatos.length == 0){
            alert("No hay datos que consultar")
            return 
        }

        this.tablehis.innerHTML = ""        
        var code=""
        for(var row of ArrayDatos){
            code+=`<tr>
                <td hidden>${row[0]}</td>
                <td >${row[1]}</td>                
                <td >${row[2]}</td>
                <td >${row[3]}</td>
                <td >${row[4]}</td>
                <td >${row[5]}</td>
                <td >${row[6]}</td>
                <td >${row[7]}</td>
                <td >${row[8]}</td>
                <td><button class="btn btn-info btndetgesase" aria-label="${row[0]}" 
                data-bs-toggle="modal" data-bs-target="#mdldetgesase"
                >Ver</button></td>
                </tr>`
        }
        this.tablehis.innerHTML =code
        
    }

    main(){
        this.btnfill.addEventListener('click',async ()=>{
            const inpfechfill = document.getElementById('inpfecgesback').value 
            if (inpfechfill==""){
                alert("Por favor selecione una fecha para consultar")
                return false
            }
            //const Callapi = new ConsultorApis(this.csrf_token)
            var Data = await new HandleApis(this.csrf_token,"/ConsultorDatos",{Option:'Gethisgesback',Fecha:inpfechfill}).callPromisePost()
            
            this.filltable(Data['Arraydatos'])
            ///Data = await this.Callapi.callpost("/ConsultorDatos",{Option:"Gethisgesback",Fecha:inpfechfill})
            
        })
    }

    async getjson(arraydatos){
        const dicdatos = {};
        for (const dato of arraydatos) {
            if (!(dato[0] in dicdatos)) {
                dicdatos[dato[0]] = [];
            }
                // Agregamos el dato a la lista correspondiente en el diccionario
                dicdatos[dato[0]].push([dato[6],dato[7],dato[8]]);

            }

        return dicdatos
    }


    async #filltablacanbase(){
        // funcion que trae los datos de las bases activas y sus asignatarios
        // creat tabla con sunn tr y con su estado en check
        // de debe crear un this.jsonestbases para registrar los checks y estados
        this.tblcanbase.innerHTML=""
        var Data = await new HandleApis(this.csrf_token,"/ConsultorDatos",{Option:'Getbasupdback'}).callPromisePost()
        var code = ""
        var arrayBasesBack = Data['Arraydatos']
        var arrayControl=[]
        var JsonDatos= await this.getjson(arrayBasesBack)
        for(var dato of arrayBasesBack){
            if ( ! arrayControl.includes(dato[0]) ){
                arrayControl.push( dato[0] );
                //agregar estadistica para comparar cambios
                // esto me va a costar mucho
                let arrayasesores = JsonDatos[dato[0]];
                this.jsonestbases[dato[0]]={"Estado":dato[2],"ArrayEstAsesores":arrayasesores}
                let codeTemp = `<tr id="${dato[0]}" name="trpadre">
                    <td hidden aria-label='${dato[0]}'>${dato[0]}</td>
                    <td><strong>${dato[1]}</strong></td>
                    <td><input class="checkbox form-check-input" type="checkbox" value="${dato[2]}" ${dato[2] == '1' ? 'checked' : ''}></td>
                    <td>${dato[3]}</td>
                    <td>${dato[4]}</td>
                    <td>${dato[5]}</td>
                    <td>
                    <select class="form-select  form-select-sm" id="selmotcamb${dato[0]}">
                        <option value="">..::Seleccione::..</option>
                         <option value="No aplica" ${dato[9] === "No aplica" ? 'selected' : ''}>No aplica</option>
                        <option value="Novedad Asesor" ${dato[9] === "Novedad Asesor" ? 'selected' : ''}>Novedad Asesor</option>
                        <option value="Cambio de gestion" ${dato[9] === "Cambio de gestion" ? 'selected' : ''}>Cambio de gestion</option>
                    </select>
                    </td>
                    <td>
                    <button class="btn btn-outline-success btn-sm">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-repeat" viewBox="0 0 16 16">
                        <path d="M11 5.466V4H5a4 4 0 0 0-3.584 5.777.5.5 0 1 1-.896.446A5 5 0 0 1 5 3h6V1.534a.25.25 0 0 1 .41-.192l2.36 1.966c.12.1.12.284 0 .384l-2.36 1.966a.25.25 0 0 1-.41-.192m3.81.086a.5.5 0 0 1 .67.225A5 5 0 0 1 11 13H5v1.466a.25.25 0 0 1-.41.192l-2.36-1.966a.25.25 0 0 1 0-.384l2.36-1.966a.25.25 0 0 1 .41.192V12h6a4 4 0 0 0 3.585-5.777.5.5 0 0 1 .225-.67Z"/>
                        </svg>

                    </button></td>
                    <td><button class="btn btn-info btn-sm" onclick="toggleCell(this)" name="${dato[0]}">+</button></td>`;

                let codeTempasesor = "";
                codeTempasesor += `
                    <tr class="extraRow" id="RowHide${dato[0]}" style="display: none;"
                `;
                for (let elements of arrayasesores) {
                    codeTempasesor += `
                        <div>
                                <td class="elemento">${elements[1]}</td>
                                <td class="elemento"><input class="checkbox form-check-input" type="checkbox" id="${elements[0]}"
                            value="${elements[2]}" ${elements[2] == '1' ? 'checked' : ''}></td>


                            </div>
                        `;
                }
                codeTempasesor += `</tr>`;
                codeTemp += codeTempasesor;
                code += codeTemp;
            }

        }
        this.tblcanbase.innerHTML = code
        this.#asigfundestab(this.csrf_token)

        }

}

