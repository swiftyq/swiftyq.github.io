$( ".expertise-item" ).on('click', function() {
	var expertise = $(this).text();
	console.log(expertise);
	$( ".btn-expertise" ).text(expertise);
})