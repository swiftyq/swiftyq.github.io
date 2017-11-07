var list_head =[
  'Swift 4 starts!',
  'I have been ready...! for a week...',
  '5 stars streaks!',
  'Headted solver in heated days!',
  'Consistent solver!',
  'How much can you be swift?',
  ''
]

var list_text = [
  'Get 4 stars by solving a problem in 5 minutes after requester post a question',
  'Turn on request push alarm for a week',
  'Get consecutive 5 stars for 10 times',
  'Solve 10 problems in 1 hour a week before exam week',
  'For 30 days, solve 1 problem each day',
  'Solve a problem in 1.5 minutes with at least 3 stars',
  ''
]

$(document).ready(function(){
  generate_grid();
  generate_list();
})
generate_grid = function(){
  for(var i=0; i<5; i++){
    $("#achievement_grid_box").append("<div id='grid_row_"+i.toString()+"' class='grid_row row'></div>")
    for(var j=0; j<24; j++){
      $("#grid_row_"+i.toString()).append("<div id='grid_"+i.toString()+"_"+j.toString()+"' class='col-sm grid'></div>")
    }
  }
  $(".grid").outerHeight(function(){
    return $(this).outerWidth();
  })
}

generate_list = function(){
  for(var i=0; i<7; i++){
    $("#achievement_list_sub_box").append("<div id='list_"+i.toString()+"' class='achievement_entity_box row'>");
    $("#list_"+i.toString()).append("<div class='col-md-2'></div><div id='list_sub_"+i.toString()+"' class='achievement_entity_sub_box col-md-10 row'></div>")
    $("#list_sub_"+i.toString()).append("<div id='list_image_"+i.toString()+"' class='achievement_entity_image col-md-3'>")
    .append("<div id='list_content_"+i.toString()+"' class='achievement_entity_exp col-md-9'>")
    $("#list_image_"+i.toString()).append("<div id='list_image_sub_"+i.toString()+"' class='achievement_entity_sub_image'></div>")
    $("#list_content_"+i.toString()).append("<div id='list_content_head_"+i.toString()+"' class='achievement_entity_head'></div>")
    .append("<div id='list_content_text_"+i.toString()+"' class='achievement_entity_text'></div>")
    $("#list_content_head_"+i.toString()).text(list_head[i]);
    $("#list_content_text_"+i.toString()).text(list_text[i]);
  }
  $("#list_sub_0").css("border-top-left-radius", "30px")
  .css("border-top-right-radius", "30px");
  $('.achievement_entity_image').outerHeight(function(){
    return $(this).outerWidth();
  })
  $('.achievement_entity_sub_image').outerHeight(function(){
    return $(this).outerWidth();
  })
}
