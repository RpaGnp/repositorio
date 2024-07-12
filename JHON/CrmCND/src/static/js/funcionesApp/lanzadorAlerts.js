async function showAlertsInfo(jsondato){
    Swal.fire({
        position: 'center',
        icon: jsondato['icon'],
        title: jsondato['Mensaje'],        
        timer: 2500,
        showConfirmButton: true,    
    })
}


async function showAlertsInfo2(jsondato){
    Swal.fire({
        position: 'center',
        icon: jsondato['icon'],
        title: jsondato['Mensaje'],                
        showConfirmButton: true,    
    })
}


async function showAlertsdec(jsondato){
    Swal.fire({
        title: jsondato['Mensaje'],        
        position: 'center',
        icon: jsondato['icon'],           
        timer: 5e3
    }).then(() => {
        window.history.back();
        // Recargar la página actual
        location.reload();
    })
    
}

// promp confirmacion
async function alertConfirmacion(jsondato){
    return new Promise((resolve) => {
        Swal.fire({
            title: jsondato['titulo'],
            text: jsondato['mensaje'],
            icon: jsondato['icono'],
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Si'
        }).then((result) => {
            resolve(result);
        });
    });
}

