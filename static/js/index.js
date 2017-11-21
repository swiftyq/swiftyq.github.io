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

$( ".fstbtn" ).on('click', function() {
  console.log($("input[name='password1']").val(), $("input[name='password2']").val());
  if ( ($( "input[type='password']").val().length)<4 || ($( "input[type='email']").val().length)<1 || ($( "input[type='expertise']").val().length)<2 || ($( "input[type='name']").val().length)<2) {
    alert("Please fill in all fields correctly");
  }
  else if ($("input[name='password1']").val() != $("input[name='password2']").val()){
    alert("Verify your password");
  }
  else {
    if ($("input[name='expertise']").val().includes("Programming")){
      $( "#modal1" ).modal('show');
      console.log('aa');
    }
    else {
      console.log($(".group .btn.btn-success.btn-block.btn-lg.title-lg").attr("type"));
      $(".group .btn.btn-success.btn-block.btn-lg.title-lg").attr("type","submit");
      $(".group .btn.btn-success.btn-block.btn-lg.title-lg").text("Proceed");
      $(".group .btn.btn-success.btn-block.btn-lg.title-lg").removeClass("btn-success");
      $(".group .btn.btn-block.btn-lg.title-lg").removeClass("fstbtn");
      $(".group .btn.btn-block.btn-lg.title-lg").addClass("btn-primary");
    }
  }
})

$( "#verylastbtn" ).on('click', function() {
  console.log("clicked");
  console.log($(".group .btn.btn-success.btn-block.btn-lg.title-lg").attr("type"));
  $(".group .btn.btn-success.btn-block.btn-lg.title-lg").attr("type","submit");
  $(".group .btn.btn-success.btn-block.btn-lg.title-lg").text("Proceed");
  $(".group .btn.btn-success.btn-block.btn-lg.title-lg").removeClass("btn-success");
  $(".group .btn.btn-block.btn-lg.title-lg").removeClass("fstbtn");
  $(".group .btn.btn-block.btn-lg.title-lg").addClass("btn-primary");
})