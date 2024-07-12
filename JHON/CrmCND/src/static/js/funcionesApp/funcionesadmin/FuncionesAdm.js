async function showPassword(elemento) {    
    // var x = document.getElementById(elemento);
    if (elemento.type === "password") {
        elemento.type = "text";
    } else {
        elemento.type = "password";
    }
  }


async function getrowselected(){
    $("#tablepw").on('click','.btn-info',async function (e){
        e.stopPropagation();
        var currentRow=$(this).closest("tr");
        var col1=currentRow.find("input:eq(1)")        
        await showPassword(col1[0]);        
    })
}

function savepass(csrf_token,asesor,supervisor){
    $("#tablepw").on('click','.btn-primary',async function (e){
        e.stopPropagation();
        var currentRow=$(this).closest("tr");
        var app=currentRow.find("td:eq(0)").text(); 
        var coluser=currentRow.find("input:eq(0)").val();         
        var colpw=currentRow.find("input:eq(1)").val();  
        const  data= await callPromise(csrf_token,"/ConsultorDatos",{Option:"updpwase",
            Usuario:asesor,sup:supervisor,apk:app,Usser:coluser,pws:colpw})        
        alert("Datos actualizados correctamente!")
        
    })
}