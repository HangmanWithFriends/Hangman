$(function() {
	
	var $email = $('#user-email-input')
	var $pwd   = $('#user-password-input')

	function isValidPassword(pwd) {
	    // at least one number, one lowercase, one uppercase letter
	    // at least nine characters
	    var re = /(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{9,}/;
	    return re.test(pwd);
	  }

	var showAlert = function(message, type) {

	    /* This stuctured mess of code creates a Bootstrap-style alert box.
	     * Note the use of chainable jQuery methods. */
	    var $alert = (
	      $('<div>')                // create a <div> element
	        .text(message)          // set its text
	        .addClass('alert')      // add some CSS classes and attributes
	        .addClass('alert-' + type)
	        .addClass('alert-dismissible')
	        .attr('role', 'alert')
	        .prepend(               // prepend a close button to the inner HTML
	          $('<button>')         // create a <button> element
	            .attr('type', 'button') // and so on...
	            .addClass('close')
	            .attr('data-dismiss', 'alert')
	            .html('&times;')    // &times; is code for the x-symbol
	        )
	        .hide()  // initially hide the alert so it will slide into view
	    );
	    
	    /* Add the alert to the alert container. */
	    $('#alerts').append($alert);

	    /* Slide the alert into view with an animation. */
	    $alert.slideDown();
	  };
	    
	$('#sign-in-form').on('submit', function(event) {
		
		event.preventDefault();

		var pwd = $('#user-password-input').val();
		var email = $('#user-email-input').val();

		if(isValidPassword(pwd)) {
		    $('#password-error').hide();
		} else {
		    $('#password-error').text('Password has to be 9 or more characters, and contain at least 1 upper case, 1 lower case, and 1 number.').show();
		    event.preventDefault();
		}
		
		/* Send the data to 'POST /users/login' to see if this username/password works */
		$.ajax({
			type : 'POST',
			url: '/users/login',
			contentType: 'application/json',
			data: JSON.stringify({
				username: email,
				password: pwd
			}),
			dataType: 'json'
		}).done(function(data) {
			var d = data;
			if(d.errors.length > 0){
				showAlert('Username/password combination is wrong', 'danger');
			}
			else{
				var uid = d.uid;
				
				window.location.href = "/users/" + uid;
			}
			
		}).fail(function() {
			showAlert('Username/password combination is wrong.', 'danger');
		});

	    });
    });

