$( ".expertise-item" ).on('click', function() {
	var expertise = $(this).text();
	console.log(expertise);
	$( ".btn-expertise" ).text(expertise);
	$(".requester_box").css("visibility", function(){
		if($(this).attr('val')==expertise){
			// $(this).css("position", "relative")
			return "visible"
		}else{
			// $(this).css("position", "absolute")
			return "hidden"
		}
	})
})

$( "#send" ).on('click', function() {
  var text = $( "textarea#chat_text" ).text();

})


$(".select_requester").on("click", function(){
	$("#previewtask_content").text($(this).attr('val2'))
})
