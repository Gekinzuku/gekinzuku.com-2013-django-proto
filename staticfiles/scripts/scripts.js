$(document).ready(function(){
  
  /* $('#slider').nivoSlider({
  	effect: 'fold',
  	slices: 10,
  	animSpeed: 400,
  	pauseTime: 5000,
  	prevText: '&larr;',
  	nextText: '&rarr;'
  }); */

  $("#nav a").mouseover(function() {
    $(this).animate({ color: "#9cddff" }, 400);
    $(this).mouseout(function() {
      $(this).animate({ color: "#ffffff" }, 400);
    });
  });

  $(".topic-even, .topic-odd").mouseover(function() {
  	$(this).children(".board-post-actions").show();
  	$(this).mouseout(function() {
  		$(this).children(".board-post-actions").hide();
  	})
  })

  $(function() {
    $( ".board-new" ).button();
    $(".topic-reply").button({
      icons: {
        primary: "ui-icon-arrowthick-1-e"
      }
    });
     $(".topic-delete").button({
      icons: {
        primary: "ui-icon-closethick"
      }
    });
    $(".close").click(function() {
    	$(".error").remove();
    })
  });

});
