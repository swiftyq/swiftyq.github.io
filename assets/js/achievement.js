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

var grid_colors = ["#aaff91",
"#75d5ff",
"#eeeeee"]
$(document).ready(function(){
  generate_grid();
  generate_list();
  achievement_pop_up("hoihoi", "dullinun");
})
generate_grid = function(){
  for(var i=0; i<5; i++){
    $("#achievement_grid_box").append("<div id='grid_row_"+i.toString()+"' class='grid_row row'></div>")
    for(var j=0; j<10; j++){
      $("#grid_row_"+i.toString()).append("<div id='grid_"+i.toString()+"_"+j.toString()+"' class='col-sm grid'></div>")
      var rand = Math.floor(Math.random()*3)
      var rand2 = Math.floor(Math.random()*100000)+100000
      //https://d30y9cdsu7xlg0.cloudfront.net/png/149821-200.png
      $("#grid_"+i.toString()+"_"+j.toString()).css("background-color", grid_colors[rand]).append("<img class='grid_img' src='https://d30y9cdsu7xlg0.cloudfront.net/png/"+rand2.toString()+"-200.png' width='0' height='0'></img>")
    }
  }
  $(".grid").outerHeight(function(){
    var height = $(this).width();
    var oh = $(this).outerWidth();
    //console.log($(this).outerWidth())
    $(".grid_img").outerWidth(height).outerHeight(height).css("margin-top", function(){
      return (oh-height)/2;
    });

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
    var rand2 = Math.floor(Math.random()*100000)+100000
    //https://d30y9cdsu7xlg0.cloudfront.net/png/149821-200.png
    $("#list_image_sub_"+i.toString()).append("<img class='list_img' src='https://d30y9cdsu7xlg0.cloudfront.net/png/"+rand2.toString()+"-200.png' width='0' height='0'></img>")

  }
  $("#list_sub_0").css("border-top-left-radius", "30px")
  .css("border-top-right-radius", "30px");

  $('.achievement_entity_image').outerHeight(function(){
    return $(this).outerWidth();
  })
  $('.achievement_entity_sub_image').outerHeight(function(){
    var height = $(this).width();
    var oh = $(this).outerWidth();
    //console.log($(this).outerWidth())
    $(".list_img").outerWidth(height).outerHeight(height).css("margin-top", function(){
      return (oh-height)/2;
    });
    return $(this).outerWidth();
  })

}
