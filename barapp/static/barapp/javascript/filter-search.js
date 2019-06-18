(function() {
  var $cocktails = $('.recipe');
  var $search    = $('#filter-search');
  var cache      = [];

  $cocktails.each(function() {
    cache.push({
      element: this,
      text: this.id.trim().toLowerCase()
    });
  });
  function filter() {
    var query = this.value.trim().toLowerCase();

    cache.forEach(function(cocktail) {
      var index = 0;
      if (query) {
        index = cocktail.text.indexOf(query);
      }

      cocktail.element.style.display = index === -1 ? 'none' : '';
    });
  }

  if ('oninput' in $search[0]) {
    $search.on('input', filter);
  } else {
    $search.on('keyup', filter);
  }
}());
