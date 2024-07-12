function main(csrf_token)
    // var csrf_token = "{{ csrf_token() }}";    
    alert(csrf_token)
    
    let jsonmeses = {1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo", 6:"Junio", 7:"Julio",
                    8:"Agosto",9:"Septiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre"};
    let date = new Date
    var mes_number = date.getMonth();
    document.getElementById('lblmesant').innerHTML= jsonmeses[mes_number]
    
    var mes_number = date.getMonth()-1
    document.getElementById('lblmesant2').innerHTML= jsonmeses[mes_number]

    $(document).ready(function () {        
        options=HeaderFetch(csrf_token,{Gestion:"GetEstadistica",IdAsesor:"{{current_user.id}}",Perfil:"{{current_user.cargo}}"})
        fetch("/AppDataBase",options).then(response => response.text())
            .then(Data => {                                
                const json = JSON.parse(Data);
                arrayBoards=['PieNotaMen','barNotaMesant','barNotaMesant2']                
                recorredor=0
                for (i in json){                    
                    const ctx = document.getElementById(arrayBoards[recorredor]);
                    recorredor+=1
                    const data = {
                    labels: ['Nota general','Criticos'],
                    datasets: [{                        
                        data: [parseFloat(json[i][0]),parseFloat(json[i][1])],
                        backgroundColor: ['rgb(51,189, 93)','rgb(199, 0, 57)'],
                        }]
                };
                new Chart(ctx, {
                type: 'pie',
                data:data,                
                options: {
                    plugins: {
                    datalabels: {
                        formatter: (value) => {
                        return value + '%';
                        },
                    },
                    },
                },
                //                                
                })                    
                }
    })
    });
    
 