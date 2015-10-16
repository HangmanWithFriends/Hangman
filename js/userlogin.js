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
			url: 'login',
			contentType: 'application/json',
			data: JSON.stringify({
				usermail: email,
				password: pwd
			}),
			dataType: 'json'
		}).done(function(data) {
			var actual_data = JSON.parse(data);
			if(acutal_data.errors.length > 0){
				window.alert('Username/password combination is wrong');
			}
			else{
                window.alert("Success")
				window.location.href = "/lobby/"+acutal_data.uid.toString()
			}
			
		}).fail(function() {
			window.alert('Could not reach server to attempt login. Try again in a few minutes.');
		});

	    });
    });

