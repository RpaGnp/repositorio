const TablaForm = new HandleForm('trnuetels')
const TablaHist = new handletabhis();
const csrf_token = document.getElementById("csrf-token").getAttribute("data-csrf");
const csrf_ciudad = document.getElementById("csrf-ciudad").getAttribute("data-csrf");
const CallAPis = new ConsultorApis(csrf_token);

document.addEventListener('DOMContentLoaded', async function() {
    await showAlertsInfo2({'icon':'info','Mensaje':'¡¡Oye!! No olvides recomendar el Uso de la App MiClaro, y 2 de sus beneficios.'})
})

document.getElementById('SelRazones').addEventListener('change', function(e) {
    TablaForm.addRow(e.target.value);
});

document.getElementById('AddNumTel').addEventListener('click', function(e) {    
    
    TablaForm.AddColTel();

});


document.getElementById('BtnGenNotas').addEventListener('click', function(e) {
    TablaForm.GenNotas()
    e.preventDefault();
})
    
document.getElementById('BtnSendBot').addEventListener('click', async function(e) {  
    DataForm = TablaForm.getjson();
    if(DataForm){  
        var DataForm = new HandleApis(csrf_token,'/AppDataBase',{"Gestion":"InsdatNotas","Ciudad":csrf_ciudad,"DataNotas":DataForm})
        var ResGes = await DataForm.callPromisePost()        
        if(ResGes){
            jsondato={'icon':'success','Mensaje':'datos enviados al Bot de gestion correctamente!'}   
            await showAlertsInfo(jsondato)
            TablaForm.reserForm();
            }
        else{
            jsondato={'icon':'error','Mensaje':'Error inesperado!'}   
            await showAlertsInfo(jsondato);
            location.reload();
        }
        
    }
    else{
        jsondato={'icon':'error','Mensaje':'verifique los campos del formulario y genere las notas correspondientes!'}   
        await showAlertsInfo(jsondato)
    }
    // location.reload()
})

document.getElementById('BtnVerHisRazon').addEventListener("click", async () => {
    // Tu código asíncrono aquí
    TablaHist.clearatble()
    var DataForm = new HandleApis(csrf_token,'/AppDataBase',{"Gestion":"Gethisrazase","Asesor":asesorId,"Ciudad":asesorCiudad })
        var ResGes = await DataForm.callPromiseGet()   
        TablaHist.Filldata(ResGes)
});

document.getElementById('btnreirazase').addEventListener("click", async () => {
    var idevento = await TablaHist.GetIdselrow()
    if (idevento){
        alert("Datos enviados al bot, Por favor espere...")
        var DataForm = new HandleApis(csrf_token,'/AppDataBase',{"Gestion":"Updreirazase","IdRazon":idevento })
        var ResGes = await DataForm.callPromisePost()
        }
    else{
        alert("Favor selecione un evento!...")
    }

})

async function cambiarEstado(){
    var idevento = await TablaHist.GetIdselrow()
    if (idevento){
        await CallAPis.callFile("ConsultorDatos",{"Option":"getimgrazon","Evento":idevento});
    }else{
        alert("Favor selecione un evento!...")
    }
    }

// actualizacion 22/04/2024 añador hsitoria de cancelaciones
async function updhistorial(){
    const tablebody=document.getElementById("tblhiscanase")
    tablebody.hinnerHTML=""
    var DataForm = new HandleApis(csrf_token,'/ConsultorDatos',{"Option":"Gethiscanase"})
    var ResGes = await DataForm.callPromiseGet()
    code=""
    for(var row of ResGes['Arraydatos']){
        code+=`<tr>
            <td hidden>${row[0]}</td>
            <td >${row[1]}</td>
            <td >${row[2]}</td>
            <td >${row[3]}</td>
            <td >${row[4]}</td>
            <td >${row[5]}</td>
        </tr>`
    }
    tablebody.innerHTML = code

  }

document.getElementById("btncallhiscan").addEventListener("click",function(){
    updhistorial()

  });