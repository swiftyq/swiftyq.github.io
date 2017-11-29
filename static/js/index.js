$("u").on('click', function() {
	$(".modal").modal('show');
})

$( ".exp" ).on('click', function() {
  var target_input = $( ".form-group input[type='expertise']" )
  var old_val = target_input.val()
  target_input.val(old_val + $(this).text() + ", ");

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
  if ( ($( "input[type='password']").val().length)<4 || ($( "input[type='email']").val().length)<1 || ($( "input[type='expertise']").val().length)<2 || ($( "input[type='name']").val().length)<2) {
    alert("Please fill in all fields correctly");
  }
  else if ($("input[name='password1']").val() != $("input[name='password2']").val()){
    alert("Verify your password");
  }
  else {
    if ($("input[name='expertise']").val().includes("Programming")){
      $( "#modal1" ).modal('show');
    }
    else {
      $(".group .btn.btn-success.btn-block.btn-lg.title-lg").attr("type","submit");
      $(".group .btn.btn-success.btn-block.btn-lg.title-lg").click()
    }
  }
})

$( ".fst-modal-btn" ).on('click', function() {
  if ($("input[name='fstmodal']").val() == "6.0"){
    $("#modal3").modal('show');
    $("#modal2").modal('hide');
  }
  else {
    $("#modal6").modal('show');
    $("#modal2").modal("hide");
  }
})

$( ".snd-modal-btn" ).on('click', function() {
  if ($("input[name='sndmodal']").val().includes("no") || $("input[name='sndmodal']").val().includes("No")){
    $("#modal4").modal('show');
    $("#modal3").modal('hide');
  }
  else {
    $("#modal6").modal('show');
    $("#modal3").modal("hide");
  }
})

$( ".trd-modal-btn" ).on('click', function() {
  if ($("input[name='trdmodal']").val().includes("1 2 3")){
    $("#modal5").modal('show');
    $("#modal4").modal('hide');
  }
  else {
    $("#modal6").modal('show');
    $("#modal4").modal("hide");
  }
})

$( "#failbutton" ).on('click', function() {
  console.log("fail");
  $.ajax({
    url: "/",
    success: function(data,status) {
      console.log("succss");
      window.location.href="/";
    }
  })
})

$( "#verylastbtn" ).on('click', function() {
  $(".group .btn.btn-success.btn-block.btn-lg.title-lg").attr("type","submit");
  $(".group .btn.btn-success.btn-block.btn-lg.title-lg").text("Proceed");
  $(".group .btn.btn-success.btn-block.btn-lg.title-lg").removeClass("btn-success");
  $(".group .btn.btn-block.btn-lg.title-lg").removeClass("fstbtn");
  $(".group .btn.btn-block.btn-lg.title-lg").addClass("btn-primary");
})
