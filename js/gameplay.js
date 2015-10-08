$(function() {
	$('#guess-form').on('submit', function(event) {
		
		event.preventDefault();

		var guess = $('#guess-input').val();
        var uid = $('#page-uid').val();
        var gid = $('#page-gid').val();
		}
		
		/* Send the data to 'POST /users/login' to see if this username/password works */
		$.ajax({
			type : 'POST',
			url: '/game/'+uid+"/"+gid,
			contentType: 'application/json',
			data: JSON.stringify({
				guessed: guess
			}),
			dataType: 'json'
		}).done(function(data) {
			var d = data;
			if(d.errors.length > 0){
			}
            else{
               location.reload(); 
			}
			
		}).fail(function() {
        });
});

