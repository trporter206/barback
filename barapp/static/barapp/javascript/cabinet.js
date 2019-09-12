function searchCocktails() {
  let cabinet = document.getElementsByClassName('cabinetItem');
  let cleanedCabinet = []
  for(c=0; c<cabinet.length; c++){
    cleanedCabinet.push(cabinet[c].innerHTML);
  }
  $.ajax({
    url: '/ajax/add_to_cabinet/',
    data: {
      'cabinet': cleanedCabinet,
    },
    dataType: 'json',
    success: function (data) {
      // data comes from views function in progress
      // add html to page here
      console.log(data);
    },
    error: console.log('ajax failed')
  });
};

function cabinetAdd() {
  let item = document.getElementById('search');
  itemval = item.value;
  let li = document.createElement("li");
  let node = document.createTextNode(itemval);
  li.appendChild(node);
  li.className += ' cabinetItem';

  let ul = document.getElementById('cabinet');
  ul.appendChild(li);
};
