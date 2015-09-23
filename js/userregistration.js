$(function() {
  function isValidEmail(email) {
    // var re = /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/;
	var re = /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9_.+-]+.[a-zA-Z0-9_.+-]+$/;
    return re.test(email);
  }

  function isValidPassword(pwd) {
    // at least one number, one letter
    // at least nine characters
    var re = /(?=.*\d)(?=.*[a-zA-z]).{7,}/;
    return re.test(pwd);
  }

  $('#register-form').on('submit', function(event) { // form id
	  
	event.preventDefault();

	var name = $('#user-name-input').val(); // input id
    var email = $('#user-email-input').val(); // input id
    var pwd = $('#user-password-input').val(); // input id

    if(isValidEmail(email)) {
      $('#email-error').hide(); // div id
    } else {
      $('#email-error').text('Email must be in the correct format.').show();
      event.preventDefault();
    }

    if(isValidPassword(pwd)) {
      $('#password1-error').hide(); // div id
    } else {
      $('#password1-error').text('Password has to be 7 or more characters, and contain at least 1 number, and 1 letter.').show();
      event.preventDefault();
    }
    $.ajax({
            type : 'POST',
            url: 'register',
            contentType: 'application/json',
            data: JSON.stringify({
                usermail: email,
                password: pwd,
                username: name
            }),
            dataType: 'json'
        }).done(function(data) {
			var d = data;
			if(d.errors.length > 0){
				showAlert('Username/password combination is wrong', 'danger');
			}
			else{
				
				window.location.href = "/lobby";
			}
			
		}).fail(function() {
			showAlert('Username/password combination is wrong.', 'danger');
		});

	    });
    });

