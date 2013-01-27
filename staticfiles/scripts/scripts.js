$(document).ready(function(){
  
  $('#slider').nivoSlider({
  	effect: 'fold',
  	slices: 10,
  	animSpeed: 400,
  	pauseTime: 5000,
  	prevText: '&larr;',
  	nextText: '&rarr;'
  });
  
  $("a").mouseover(function() {
    $(this).animate({ color: "#9cddff" }, 400);
    $(this).mouseout(function() {
      $(this).animate({ color: "#ffffff" }, 400);
    });
  });

});
