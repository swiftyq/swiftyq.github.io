$("u").on('click', function() {
	$(".modal").modal('show');
})

$( ".dropdown-menu a" ).on('click', function() {
  console.log($(this).text());
  var target_input = $( ".form-group input[type='expertise']" )
  var old_val = target_input.val()
  target_input.val(old_val+$(this).text()+", ");
})

$( "#btn-signup" ).on('click', function() {
  $( ".modal.fade" ).show();
  alert("clicked");
})

$( "#verylastbtn" ).on('click', function() {
  window.location.href = "index.html";
})