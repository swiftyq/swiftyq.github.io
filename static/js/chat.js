 $("#prompt form").submit(function(e) {
 
      // close the overlay
      triggers.eq(1).overlay().close();
 
      // get user input
      var input = $("input", this).val();
 
      // do something with the answer
      triggers.eq(1).html(input);
 
      // do not submit the form
      return e.preventDefault();
  });
  