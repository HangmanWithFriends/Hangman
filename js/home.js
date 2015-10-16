$(function() {
	$('#guest-login').on('submit', function(event) {
		
		event.preventDefault();
	
		/* Send the data to 'GET /guestlobby' to receive a uid */
		$.ajax({
			type : 'GET',
			url: 'get-guest-uid'
		}).done(function(data) {
			var d = data;
			var actual_json = JSON.parse(d);
			console.log(actual_json.uid);
			window.location.href = "/guestlobby/" + actual_json.uid;
			
		}).fail(function() {
			window.alert('Username/password combination is wrong.', 'danger');
		});

	    });
    });

