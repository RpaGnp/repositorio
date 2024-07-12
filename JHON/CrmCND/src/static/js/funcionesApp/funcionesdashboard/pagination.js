
function DisplayList (items, wrapper, rows_per_page, page) {
  wrapper.innerHTML = "";
  page--;

  let start = rows_per_page * page;
  let end = start + rows_per_page;
  let paginatedItems = items.slice(start, end);

  for (let i = 0; i < paginatedItems.length; i++) {
    let item = paginatedItems[i];

    let row_element = document.createElement('tr');
    row_element.classList.add('item');
    wrapper.appendChild(row_element);

    for(var ci=0;ci<=5;ci++){
      let td = document.createElement('td');
      if (ci==0){td.style="display:none;";td.id="pathDw";td.innerText = item[ci]}
      else if(ci==4){
        alink=document.createElement("a")
        alink.href = item[ci]
        alink.target="_blank"
        alink.innerHTML="Link"
        td.appendChild(alink)
      }
      else if (ci==5){             
          ArrayBotones=[["Ver","btndwpret"],["Editar","btnedipreturno"],["Eliminar","btndelpret"],["Upd Notas","btncarnotpre"]]//["Asistencia","btnasispre"]
          for (let btn of ArrayBotones) {
            btns = document.createElement("button");
            btns.classList.add("btn");
            btns.id=btn[1]
            btns.innerHTML=btn[0]
            td.appendChild(btns)};
          }
      else{
        td.innerText = item[ci];
      }
      row_element.appendChild(td);
      wrapper.appendChild(row_element);
      }

  }
  }


function SetupPagination (items, wrapper, rows_per_page,page) {
  wrapper.innerHTML = "";

  let page_count = Math.ceil(items.length / rows_per_page);
  for (let i = 1; i < page_count + 1; i++) {
    let btn = PaginationButton(i, items,page);
    wrapper.appendChild(btn);
  }
}

function PaginationButton (page, items,current_page) {
  let button = document.createElement('button');
  button.classList.add('page-link')
  button.innerText = page;

  if (current_page == page) button.classList.add('active');

  button.addEventListener('click', function () {
    current_page = page;
    DisplayList(items, list_element, rows, current_page);

    let current_btn = document.querySelector('.pagenumbers button.active');
    current_btn.classList.remove('active');

    button.classList.add('active');
  });

  return button;
}
  