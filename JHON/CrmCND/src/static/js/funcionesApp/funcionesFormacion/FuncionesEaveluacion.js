        class HandleSelePre{
            constructor(ciudad,idasesor,cargo){
                this.csrf_token=document.getElementById('csrf-token').getAttribute('data-csrf')
                this.selpretmes=document.getElementById('selectpreturno')
                this.ciudad = ciudad
                this.idasesor = idasesor
                this.cargo = cargo
            }

            async addpretsel(ArrayPret){
                this.selpretmes.innerText=""
                for(var dato of ArrayPret){
                    console.log(dato)
                    var opt = document.createElement("option")
                    opt.setAttribute("value",dato[0])
                    opt.innerText= dato[1]
                    this.selpretmes.appendChild(opt)
                }
            }

            async addclickMes(){
                var mes  = document.getElementById("selectmes").value;                                
                var Data = await new HandleApis(this.csrf_token,'/ConsultorDatos',{
                    Option:'Getpretmes',mesdata:mes,yeardata:new Date().getFullYear() ,"CiuData":this.ciudad,"IdAsesor":this.idasesor}).callPromisePostJson()
                    await this.addpretsel(Data)
                }
            
           
            
            async AddEvaByPreTbl(){
                var Tabla = document.getElementById('tbldetevabypre');
                var idPre = document.getElementById("selectpreturno").value;                
                Tabla.innerHTML=""                              
                var Data = await new HandleApis(this.csrf_token,'/AppDataBase',{
                    Gestion:'GetEstevabypre',"IdPreturno":idPre}).callPromisePostJson()                    
                    for(var array of Data['Evaluaciones']){
                        var tr=document.createElement("tr")
                        tr.innerHTML=`<td>${array[0]}</td><td>${array[1]}</td><td>${array[2]}</td><td>${array[3]}</td><td>${array[4]}</td><td>${array[5]}</td>`
                        Tabla.appendChild(tr)
                    }

            }

            addFuncMes(){
                document.getElementById("selectmes").addEventListener("change",async (e)=>{
                    var Data = await new HandleApis(this.csrf_token,'/ConsultorDatos',{
                        Option:'Getevabypre',mesdata:e.target.value,"CiuData":this.ciudad,"IdAsesor":this.idasesor}).callPromisePost()
                        this.addpretsel(Data)
                })
            }
            
            addFuncPre(){
                document.getElementById("selectpreturno").addEventListener("change",()=>{
                    this.AddEvaByPreTbl()
                })
            }
        }

        class HandleFiles {
            async getbytesfile(elemento) {
                return new Promise((resolve, reject) => {
                    const file = elemento.files[0];
                    const Name = file.name;
                    const reader = new FileReader();

                    reader.onload = (event) => {
                        const fileContent = event.target.result;
                        const data = { NombreFile: Name, BinarioFile: fileContent };
                        resolve(data);
                    };

                    reader.readAsDataURL(file);
                });
            }
        }

        class HandlePreguntas{
            constructor(idasesor){
                this.numeropreguntas=0
                this.ArrayGralPreguntas=[]
                this.idasesor =idasesor
                this.csrf_token=document.getElementById('csrf-token').getAttribute('data-csrf')
            }

            #aumnumpre(){
                this.numeropreguntas+=1
            }

            #disnumpre(){
                this.numeropreguntas-=1
            }


            async conspreg(){
                const boar=document.getElementById('BoardConst')
                const newDiv = document.createElement("div");
                newDiv.classList.add("shadow", "p-3", "mb-5", "bg-body", "rounded");               
                this.#aumnumpre()
                // codigo para crear un campo para crear preguntas
                var code=`
                <div class="card text-center shadow p-3 mb-5 bg-body rounded" style="border: radius black 1px" >
                    <h5 class="card-title">Pregunta N°:`+this.numeropreguntas+`</h5>
                    <div class="card-header">                        
                    </div>
                        <div class="card-body" class="tab-content" style="text-align: start;">                            
                            <div id="Preguntas" data-tab-content class="active">                    
                                <div class="form-floating">
                                    <textarea class="form-control floatingTextarea" rows="4" id="floatingTextarea`+this.numeropreguntas+`" required></textarea>
                                    <label for="floatingTextarea">Pregunta</label>
                                </div>
                            </div>
                            <div id="Repuestas" data-tab-content>
                                <label for="SelTipPre"  class="form-label">Tipo de Pregunta</label>
                                <select name="SelTipPre" id="SelTipPre`+this.numeropreguntas+`" class="form-select SelTipPre" required>
                                    <option value="">Seleccione...</option>
                                    <option value="1b">Falso/Verdadero</option>
                                    <option value="2b">Multiple</option>
                                    <option value="3b">Ordenar</option>
                                </select>
                                <div id="divCreaPre`+this.numeropreguntas+`">

                                </div>
                            </div>
                            <div id="Multimedia" data-tab-content>                            
                                <label for"formFile">Seleccione un archivo</label>
                                <input class="form-control" type="file"accept="image/jpeg, image/png"  id="formFile`+this.numeropreguntas+`">
                            </div>
                            <hr>                                
                            <input type="button" value="Eliminar" id="btnDelPreg`+this.numeropreguntas+`" class="btn btn-danger btnDelPreg">
                        
                    </div>
                </div>
                <hr>
                    `
                newDiv.innerHTML=code
                //const newContent = document.createTextNode("Hi there and greetings!");
                // newDiv.appendChild(newContent);
                const currentDiv = document.getElementById("div1");
                document.body.insertBefore(newDiv, currentDiv);
                boar.appendChild(newDiv)

                var Items =document.querySelectorAll('.SelTipPre')
                for(var element of Items){
                    element.addEventListener("change", (e)=>{                                                                                
                    this.CamTipPreg(e.target.value)
                    })
                }

                var ItemsDel=document.querySelectorAll('.btnDelPreg')
                for(var element of ItemsDel){
                    element.addEventListener("click", (e)=>{                                                                                                        
                        this.DelPregunta(e.target)
                    })
                }
                
            }


            async DelPregunta(iddiv){
                let divpregunta = document.getElementById(iddiv.getAttribute("id")).closest('.card'); // Reemplaza 'clase-comun' con la clase compartida
                // let divpregunta = document.getElementById(iddiv.getAttribute("id")).parentNode.parentNode.parentNode.parentNode.parentNode
                divpregunta.remove()
                this.#disnumpre()
            }

            async CamTipPreg(Tipo){                
                var OptGet=Tipo
                var boarRes=document.getElementById('divCreaPre'+this.numeropreguntas)
                boarRes.innerHTML=""
                var newDivRes = document.createElement("div");                        
                if(OptGet=='1b'){
                    var code=`
                    <table class="table">
                        <thead>
                        <tr>
                            <th>Opción</th>
                            <th>Correcta</th>
                        </tr>
                        </thead>
                        <tbody>
                        <tr>
                            <td>Verdadero</td>
                            <td><Input id="chkTrue`+this.numeropreguntas+`" class="form-check-input" type="checkbox"></Input></td>
                        </tr>
                        <tr>
                            <td>Falso</td>
                            <td><Input id="chkFalse`+this.numeropreguntas+`" class="form-check-input" type="checkbox"></Input></td>
                        </tr>
                        </tbody>
                    </table>
                `
                
                }else if(OptGet=='2b'){
                    var code=`
                    <table class="table">
                    <thead>
                    <tr>
                        <th>Opción</th>
                        <th>Correcta</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr>
                        <td>
                            <div class="form-floating">
                                <textarea class="form-control" placeholder="Escriba su opcion de respuesta" id="textResA`+this.numeropreguntas+`"></textarea>
                                <label for="textResA">A</label>
                            </div>
                        </td>
                        <td>
                            <Input class="form-check-input" type="checkbox" id="checkResA`+this.numeropreguntas+`"></Input>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <div class="form-floating">
                                <textarea class="form-control" placeholder="Escriba su opcion de respuesta" id="textResB`+this.numeropreguntas+`"></textarea>
                                <label for="textResB">B</label>
                            </div>
                        </td>
                        <td>
                            <Input class="form-check-input" type="checkbox" id="checkResB`+this.numeropreguntas+`"></Input>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <div class="form-floating">
                                <textarea class="form-control" placeholder="Escriba su opcion de respuesta" id="textResC`+this.numeropreguntas+`"></textarea>
                                <label for="textResC">C</label>
                            </div>
                        </td>
                        <td>
                            <Input class="form-check-input" type="checkbox" id="checkResC`+this.numeropreguntas+`"></Input>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <div class="form-floating">
                                <textarea class="form-control" placeholder="Escriba su opcion de respuesta" id="textResD`+this.numeropreguntas+`"></textarea>
                                <label for="textResD">D</label>
                            </div>
                        </td>
                        <td><Input class="form-check-input" id="checkResD`+this.numeropreguntas+`" type="checkbox"></Input></td>
                    </tr>
                    </tbody>
                </table>
                    
                `
                }
                else if ('3b'){
                    var code=`
                    <table class="table">
                    <thead>
                    <tr>
                        <th>Opción</th>
                        <th>Correcta</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr>
                        <td>
                            <div class="form-floating">
                                <textarea class="form-control" placeholder="Escriba su opcion de respuesta" id="textResOrd1`+this.numeropreguntas+`"></textarea>
                                <label for="textResOrd1`+this.numeropreguntas+`">A</label>
                            </div>
                        </td>
                        <td>
                            <select name="" id="selordpreg1`+this.numeropreguntas+`" class="form-select" required>
                                <option value="">Seleccione...</option>
                                <option value="01">1</option>
                                <option value="02">2</option>
                                <option value="03">3</option>
                                <option value="04">4</option>
                                <option value="05">5</option>
                            </select>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <div class="form-floating">
                                <textarea class="form-control" placeholder="Escriba su opcion de respuesta" id="textResOrd2`+this.numeropreguntas+`"></textarea>
                                <label for="textResOrd2`+this.numeropreguntas+`">B</label>
                            </div>
                        </td>
                        <td>
                            <select name="" id="selordpreg2`+this.numeropreguntas+`" class="form-select" required>
                                <option value="">Seleccione...</option>
                                <option value="01">1</option>
                                <option value="02">2</option>
                                <option value="03">3</option>
                                <option value="04">4</option>
                                <option value="05">5</option>
                            </select>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <div class="form-floating">
                                <textarea class="form-control" placeholder="Escriba su opcion de respuesta" id="textResOrd3`+this.numeropreguntas+`"></textarea>
                                <label for="textResOrd3`+this.numeropreguntas+`">C</label>
                            </div>
                        </td>
                        <td>
                            <select name="" id="selordpreg3`+this.numeropreguntas+`" class="form-select" required>
                                <option value="">Seleccione...</option>
                                <option value="01">1</option>
                                <option value="02">2</option>
                                <option value="03">3</option>
                                <option value="04">4</option>
                                <option value="05">5</option>
                            </select>
    
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <div class="form-floating">
                                <textarea class="form-control" placeholder="Escriba su opcion de respuesta" id="textResOrd4`+this.numeropreguntas+`"></textarea>
                                <label for="textResOrd4`+this.numeropreguntas+`">D</label>
                            </div>
                        </td>
                        <td>
                            <select name="" id="selordpreg4`+this.numeropreguntas+`" class="form-select" required>
                                <option value="">Seleccione...</option>
                                <option value="01">1</option>
                                <option value="02">2</option>
                                <option value="03">3</option>
                                <option value="04">4</option>
                                <option value="05">5</option>
                            </select>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <div class="form-floating">
                                <textarea class="form-control" placeholder="Escriba su opcion de respuesta" id="textResOrd5`+this.numeropreguntas+`"></textarea>
                                <label for="textResOrd5`+this.numeropreguntas+`">E</label>
                            </div>
                        </td>
                        <td>
                            <select name="" id="selordpreg5`+this.numeropreguntas+`" class="form-select" required>
                                <option value="">Seleccione...</option>
                                <option value="01">1</option>
                                <option value="02">2</option>
                                <option value="03">3</option>
                                <option value="04">4</option>
                                <option value="05">5</option>
                            </select>
                        </td>
                    </tr>
                    </tbody>
                </table>
                    
                `
                }else{
                    
    
                }
    
                newDivRes.innerHTML=code
                boarRes.appendChild(newDivRes)
            }
        
        async #getsizeTable(){
            var rows =document.getElementById('tbldetevabypre').children
            console.log(rows)
            return rows.length
        }

        async CreJsonPre(){
            // recoge los inputs y crea un string tipo dicionario            
            var IdPret = document.getElementById("selectpreturno").value;
            var Rows = await this.#getsizeTable()
            if ( Rows >=1 ){
                showAlertsInfo2({'icon':"error",'Mensaje':'Ya existe una evaluacion para este preturno, no es posible crear otra, valide con el administrador de sistema!'})
                return
            }

            if(this.numeropreguntas == 0){
                showAlertsInfo2({'icon':"error",'Mensaje':'No hay preguntas creadas!'})
                return
            }
            const HandleArchivos = new HandleFiles()
            this.ArrayGralPreguntas=[]                
            for(var i=1;i<=this.numeropreguntas;i++){                
                var jsonPregunta={}                    
                jsonPregunta.Pregunta = document.getElementById('floatingTextarea'+i).value;
                jsonPregunta.TipoPregunta = document.getElementById('SelTipPre'+i).value;                        
                jsonPregunta.IdPregunta = i
                var opcionrespuesta=  jsonPregunta['TipoPregunta']
                
                var respuesta=document.getElementById("SelTipPre"+i).value 
                if(opcionrespuesta==""){
                    alert("Debe diligenciar todos los campos!")
                    return
                }                    
                var jsonVF={}
                if (opcionrespuesta=="1b"){                        
                    jsonVF.Verdadero=document.getElementById('chkTrue'+i).checked
                    jsonVF.Falso=document.getElementById('chkFalse'+i).checked                    
                    jsonPregunta.ResPre=jsonVF

                }else if(opcionrespuesta=="2b"){                                          
                    var arrayInputs=["textResA","textResB","textResC","textResD"]
                    var arrayChecks=["checkResA","checkResB","checkResC","checkResD"]
                    for(var j=0;j<arrayInputs.length;j++){                        
                        var pregunta=document.getElementById(arrayInputs[j]+i).value;    
                        var respuesta=document.getElementById(arrayChecks[j]+i).checked;                        
                        jsonVF[pregunta] = respuesta;  
                        jsonPregunta.ResPre=jsonVF                           
                    }                    
                }else{
                    for(var j=1;j<6;j++){
                        jsonVF[document.getElementById("textResOrd"+j+i).value]=document.getElementById("selordpreg"+j+i).value
                        jsonPregunta.ResPre=jsonVF                           
                    }
                }

                if(document.getElementById("formFile"+i).files.length > 0){
                    var  BinarioFile = await HandleArchivos.getbytesfile(document.getElementById("formFile"+i))
                    jsonPregunta.Files= BinarioFile
                }

                var jsonTemp = {}                    
                jsonTemp[i] = jsonPregunta                                                         
                this.ArrayGralPreguntas.push(jsonTemp)
                }                      
            var DataForm = new HandleApis(this.csrf_token,'/AppDataBase',{"Gestion":"Insdateva","IdPret":IdPret,"JsonEva":this.ArrayGralPreguntas,"Asesor":this.idasesor }).callPromisePost()
            showAlertsInfo({'icon':"success",'Mensaje':'evaluacione creada con exito!'})
               
            
        }
    }


        

    class HandleTblAse{
        constructor(csrf_token,IdAsesor,cargo){
            this.csrf_token=csrf_token
            this.tblNotas = document.getElementById("tblnotaevapre")
            this.selpret = document.getElementById("selectpreturno")
            this.cargo = cargo
            this.idasesor =IdAsesor
            this.CallAPis = new ConsultorApis(this.csrf_token)
        }

        async #resetTable(){
            this.tblNotas.innerHTML=""
        }

        async Selectedrow(){
            $('.table-row').click(function() {
                $('.table-row').removeClass('selected-row');
                $(this).addClass('selected-row');
            })
        }

        async Filldata(data){
            data['AseEval'].forEach(element => {
                var tr = document.createElement("tr")
                tr.classList.add('table-row');
                tr.innerHTML = `<td>${element[0]}</td> <td>${element[1]}</td> <td>${element[2]}</td> <td>${element[3]}</td> <td>${element[4]}</td><td>${element[5]}</td><td>${element[6]}</td>`;
                this.tblNotas.appendChild(tr)
            })
            await this.Selectedrow()
        }


        async filltableSup(){            
            await this.#resetTable();
            var idPre =this.selpret.value                        
            var DataForm = await new HandleApis(this.csrf_token,'/AppDataBase',{"Gestion":"GetNoteprebysup","IdPreturno":idPre,"Idsuper":this.idasesor}).callPromisePost()            
            await this.Filldata(DataForm)

        }


        async filltable(){
            await this.#resetTable();
            var idPre =this.selpret.value                        
            var DataForm = await new HandleApis(this.csrf_token,'/AppDataBase',{"Gestion":"GetNotasebypre","IdPreturno":idPre}).callPromisePost()            
            await this.Filldata(DataForm)
        }

        async addfuncsel(){
            this.selpret.addEventListener("change",()=>{                
                this.filltable()
                
            })
        }

        async getdatase(){
            switch (this.cargo){
                case "SUPERVISOR":
                    this.filltableSup()
                    break
                default:
                    this.filltable()
                    break
            }
        }


        async DwResPreAse(){
            Array.from(this.tblNotas.querySelectorAll("tr")).forEach(async  (fila) =>{
                if (fila.classList.contains("selected-row")) {
                    // Obtén todas las celdas de la fila
                    const idEvaluacion = fila.textContent.split(" ")[0];
                    var DataForm = await this.CallAPis.callFile('/ConsultorDatos',{"Option":"getcomresase","IdEvaluacion":idEvaluacion})
                    return DataForm
                }
            });

        }

        async DwResPre(idPreturno){
            await this.CallAPis.callFile('/ConsultorDatos',{"Option":"GetNotEvaPre","IdPreturno":idPreturno})
        }

    }