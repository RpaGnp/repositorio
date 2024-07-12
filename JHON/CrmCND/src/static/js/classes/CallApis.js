class HandleApis{
    constructor(csrf_token,api,JsonDatos){                 
        this._optionsPost = {
            method: "POST",
            headers: {
                'Accept': 'application/json, text/plain, */*',
                'Content-Type': 'application/json',
                "X-CSRFToken": csrf_token,
            },
            
            body: JSON.stringify(JsonDatos),        
            };
        
        this._optionsGet = {
                method: "GET",
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    "X-CSRFToken": csrf_token,
                },
                body: JSON.stringify(JsonDatos),
            }
        this.api=api;
    }


    async callPromisePost(){
        var list_items=[]
            await fetch(this.api,this._optionsPost).then(response => response.text()).then(data => {
                try{        
                    list_items = JSON.parse(data);                                            
                }catch(error){
                    list_items = error
                }
            }).catch((error) => {
                console.log('Error:', error);}
            )
            return list_items;
        }
    
    async callPromisePostJson(){
        var list_items=[]
        await fetch(this.api,this._optionsPost).then(response => response.json()).then(data => {        
            list_items  = data;            
        }).catch((error) => {
            console.log('Error:', error);}
        )
        return list_items;
        }


    async callPromiseGet(){
            var list_items=[]
                await fetch(this.api,this._optionsPost).then(response => response.json()).then(data => {
                    try{        
                        list_items = data;                                            
                    }catch{
                        list_items = false
                    }
                }).catch((error) => {
                    console.log('Error:', error);}
                )
                return list_items;
            }
    }



class ConsultorApis{
    constructor(csrf_token){
        this.csrf_token =csrf_token
    }

    async #preparampost(JsonDatos){
        var _optionsPost = {
            method: "POST",
            headers: {
                'Accept': 'application/json, text/plain, */*',
                'Content-Type': 'application/json',
                "X-CSRFToken": this.csrf_token,
            },
            
            body: JSON.stringify(JsonDatos),        
            };
        return _optionsPost
    }

    async callpost(api,JsonDatos){
        var optionsPost= await this.#preparampost(JsonDatos)
        var list_items=[]
            await fetch(api,optionsPost).then(response => response.text()).then(data => {
                try{        
                    list_items = JSON.parse(data);                                            
                }catch(error){
                    list_items = error
                }
            }).catch((error) => {
                console.log('Error:', error);}
            )
            return list_items;

    }

    async callFile(api,JsonDatos){
        var optionsPost= await this.#preparampost(JsonDatos)
        fetch(api,optionsPost)
        .then(async response => {
            if (!response.ok) {
              throw new Error('La solicitud no fue exitosa');
            }
            // Obtener el nombre del archivo del encabezado 'Content-Disposition'
            const contentDisposition = response.headers.get('Content-Disposition');
            const matches = contentDisposition.match(/filename=["']?([^'"\s]+)["']?/);

            if (matches && matches[1]) {
                var nombreArchivo = matches[1];
              } else {
                console.log('No se pudo extraer el nombre del archivo');
              }

            // Devolver el flujo de datos como Blob y el nombre del archivo
            const blob = await response.arrayBuffer();
            return { blob: blob, nombreArchivo };
          })
          .then(({ blob, nombreArchivo }) => {
            // Construir el Blob a partir del array de bytes
            const nuevoBlob = new Blob([blob], { type: 'application/octet-stream' });

            // Crear el objeto URL solo si la construcción del Blob fue exitosa
            const url = window.URL.createObjectURL(nuevoBlob);

            const a = document.createElement('a');
            a.href = url;
            a.download = nombreArchivo; // Utilizar el nombre del archivo obtenido
            document.body.appendChild(a);
            a.click();

            // Revocar el objeto URL después de su uso
            window.URL.revokeObjectURL(url);
          })
          .catch(error => {
            console.error('Error al descargar el archivo:', error);
          });
        }

}