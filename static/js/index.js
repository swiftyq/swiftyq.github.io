$("u").on('click', function() {
	$(".modal").modal('show');
})

$( ".dropdown-menu a" ).on('click', function() {
  console.log($(this).text());
  var target_input = $( ".form-group input[type='expertise']" )
  var old_val = target_input.val()
  target_input.val(old_val+$(this).text()+", ");
})
$("#field_reset").on("click", function(){
	 $('#expertise_button').prop('disabled', false);
	 $("#expertise").val('');
})
$( "#btn-signup" ).on('click', function() {
  $( ".modal.fade" ).show();
  alert("clicked");
})
//<<<<<<< HEAD

$( "#verylastbtn" ).on('click', function() {
  window.location.href = "index.html";
})
//=======
//>>>>>>> d9fbd65940f66ae4c3b4f48583a65730bed64a38
