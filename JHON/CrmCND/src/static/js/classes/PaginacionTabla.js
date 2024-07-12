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

        for(var ci=0;ci<8;ci++){
        let td = document.createElement('td');
        if (ci==0){td.style="display:none;";td.id="pathDw";td.innerText = item[ci]}
        else if(ci==6){
            alink=document.createElement("a")
            alink.href = item[ci]
            alink.target="_blank"
            alink.innerHTML="Link"
            td.appendChild(alink)
        }
        else if (ci==7){
                let html = `<div class="dropdown">
                  <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    Acciones
                  </button>
                  <div class="dropdown-menu" aria-labelledby="dropdownMenuButton" style="border:solid">
                    <button class="dropdown-item" id="btndwpret">Ver</button>
                    <button class="dropdown-item" id="btnedipreturno">Editar</button>
                    <button class="dropdown-item" id="btndelpret">Eliminar</button>
                    <button class="dropdown-item" id="btnasispre">Asistencia</button>
                  </div>
                </div>`
                td.innerHTML=html

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