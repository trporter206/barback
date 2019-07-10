$('.nav-tabs').each(function(){
  var $this  = $(this);
  var $tab   = $this.find('li');
  var $link  = $tab.find('a.active');
  var $panel = $($link.attr('href'));

  $this.on('click', '.nav-link', function(e) {
    e.preventDefault();
    var $link = $(this);
    var id    = this.hash;

    if (id && !$link.is('.active')) {
      $panel.removeClass('active');
      $tab.removeClass('active');

      $panel = $(id).addClass('active');
      $tab   = $link.parent().addClass('active');
    }
  });
});
