$(function() {
	
	var $email = $('#user-email-input')
	var $pwd   = $('#user-password-input')

   
	$('#login-form').on('submit', function(event) {
		event.preventDefault();

		var pwd = $('#user-password-input').val();
		var email = $('#user-email-input').val();

		/* Send the data to 'POST /login' to see if this username/password works */
		$.ajax({
			type : 'POST',
			url: '/login',
			contentType: 'application/json',
			data: JSON.stringify({
				usermail: email,
				password: pwd
			}),
			dataType: 'json'
		}).done(function(data) {
			var d = data;
			if(d.errors.length > 0){
				window.alert('Username/password combination is wrong');
			}
			else{
				// Get user id
				var uid = d.result;
				console.log(uid);
				window.location.href = "/lobby/" + uid;
			}
			
		}).fail(function() {
			window.alert('Could not reach server to attempt login. Try again in a few minutes.');
		});

	    });
    });

