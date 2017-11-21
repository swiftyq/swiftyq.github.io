achievement_pop_up = function(title, content){
  $('body').prepend("<div id='achievement_pop_up_container' class='col-md-12'></div>").prepend('<div id="achievement_pop_up_overlay"></div>')
  $('#achievement_pop_up_container').append("<div id='list_pop_up' class='achievement_entity_box row'>");
  $("#list_pop_up").append("<div class='col-md-2'></div><div id='list_sub_pop_up' class='achievement_entity_sub_box col-md-10 row'></div>")
  $("#list_sub_pop_up").append("<div id='list_image_pop_up' class='achievement_entity_image col-md-3'>")
  .append("<div id='list_content_pop_up' class='achievement_entity_exp col-md-9'>")
  $("#list_image_pop_up").append("<div id='list_image_sub_pop_up' class='achievement_entity_sub_image'></div>")
  $("#list_content_pop_up").append("<div id='list_content_head_pop_up' class='achievement_entity_head'></div>")
  .append("<div id='list_content_text_pop_up' class='achievement_entity_text'></div>")
  $("#list_content_head_pop_up").text(title);
  $("#list_content_text_pop_up").text(content);
  $("#achievement_pop_up_container").prepend("<div id='achievement_title_pop_up' class='achievement_head'></div>").append("<div id='achievement_orna_1'></div>")
  $("#achievement_title_pop_up").text("You made an achievement!")
  $("#list_content_pop_up").append("<button id='close_achievement' class='btn btn-success'>Yay!</button>")
  var rand2 = Math.floor(Math.random()*20)
  //https://d30y9cdsu7xlg0.cloudfront.net/png/149821-200.png
  $("#list_image_sub_pop_up").append("<img class='list_pop_img' src='static/achievement/icon/"+rand2.toString()+"-200.png' width='0' height='0'></img>")
  $('#list_image_pop_up').outerHeight(function(){
    return $(this).outerWidth();
  })
  $('#list_image_sub_pop_up').outerHeight(function(){
    var height = $(this).width();
    var oh = $(this).outerWidth();
    //console.log($(this).outerWidth())
    $(".list_pop_img").outerWidth(height).outerHeight(height).css("margin-top", function(){
      return (oh-height)/2;
    });
    return $(this).outerWidth();
  })
  $("#close_achievement").on("click", function(){
    $("#achievement_pop_up_overlay").remove();
    $("#achievement_pop_up_container").remove();
    $("#achievement_pop_up_overlay").remove();
  })
}
