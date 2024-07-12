



function CreaTablaRow(list_items){
    jasonCols ={ "Col0":"td.style='display:none;';td.id='pathDw';td.innerText = items[0]",
                  "Col1":"td.innerText = items[1];","Col2":"td.innerText = items[2];","Col3":"td.innerText = items[3];",
                  "Col4":"alink=document.createElement('a');alink.href = items[4];alink.target='_blank';alink.innerHTML='Link';td.appendChild(alink)"
                  }
        for(items of list_items){
          var td = document.createElement('td');
          for(key in jasonCols){            
            eval(jasonCols[key])
          }
          row_element.appendChild(td);
          tablaPreturnos.appendChild(row_element);
        }

}