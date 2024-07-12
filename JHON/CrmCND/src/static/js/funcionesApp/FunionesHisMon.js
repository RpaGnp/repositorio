function ExpanderDetalles(){
    $(this).toggleClass("btn-success btn-warning");
    
    $(this).children("span").toggleClass("glyphicon-search glyphicon-zoom-out");  
    
    $(this).closest("tr").next("tr").toggleClass("hide");
    
    if($(this).closest("tr").next("tr").hasClass("hide")){
      $(this).closest("tr").next("tr").children("td").slideUp();
    }
    else{
      $(this).closest("tr").next("tr").children("td").slideDown(350);
    }
}
  
var HadleBusquedas = new HandleCardBusqeda
document.getElementById("datatable-search-input").addEventListener("keyup",function(e){
  HadleBusquedas.ResetTable()
});


document.getElementById("Btnbusdata").addEventListener("click",function(){
  HadleBusquedas.GetFilterData()
});

document.getElementById('btnconcasmon').addEventListener('click',function(){
  HadleBusquedas.filltablemon()
})






