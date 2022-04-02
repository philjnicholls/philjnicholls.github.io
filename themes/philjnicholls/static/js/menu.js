$( document ).ready(function() {
  const menu = new MmenuLight( document.querySelector( '#menu' ), 'all');
  var navigator = menu.navigation({
    selectedClass: 'Selected',
    slidingSubmenus: true,
    theme: 'light',
    title: ''
  });
  var drawer = menu.offcanvas({
    position: 'left'
  });
  document.querySelector( 'a[href="#menu"]' )
    .addEventListener( 'click', evnt => {
      evnt.preventDefault();
      drawer.open();
    });
});
