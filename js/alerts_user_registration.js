$(function() {
  function isValidEmail(email) {
    // var re = /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/;
	var re = /^[a-zA-Z0-9_.+-]+@nd.edu$/;
    return re.test(email);
  }

  function isValidPassword(pwd) {
    // at least one number, one lowercase, one uppercase letter
    // at least nine characters
    var re = /(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{9,}/;
    return re.test(pwd);
  }

  function isValidPhone(phone) {
    // phone must be all digits
    var re = /^\d*$/;
    return re.test(phone);
  }
  
  function isValidAge(age) {
	  // age must be all digits
	  var re = /^\d*$/;
	  return re.test(age);
  }

  function passwordsMatch(pwd, pwd_conf){
	  return pwd == pwd_conf
  }

  /* A function to show an alert box at the top of the page. */
  var showAlert = function(message, type) {

    /* This stuctured mess of code creates a Bootstrap-style alert box.
 *      * Note the use of chainable jQuery methods. */
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

  $('#user-add-form').on('submit', function(event) { // form id
    var firstname = $('#user-firstname-input').val();
    var lastname = $('#user-lastname-input').val();
    var email = $('#user-email-input').val(); // input id
    var age = $('#user-age-input').val();	// input id
    var pwd = $('#user-password-input').val(); // input id
    var pwd_conf = $('#user-password-input-confirm').val(); // input id
    var submit = true
    if(isValidEmail(email)) {
      $('#email-error').hide(); // div id
    } else {
      $('#email-error').text('Email must be an @nd.edu account.').show();
      event.preventDefault();
      submit = false
    }

    if(isValidAge(age)){
    	$('#age-error').hide();
    } else {
    	$('#age-error').text('Age must contain only digits.').show();
    	event.preventDefault();
        submit = false
    }
    if(isValidPassword(pwd)) {
      $('#password1-error').hide(); // div id
    } else {
      $('#password1-error').text('Password has to be 9 or more characters, and contain at least 1 upper case, 1 lower case, and 1 number.').show();
      event.preventDefault();
      submit = false
    }
    if(isValidPassword(pwd_conf)) {
	    $('#password2-error').hide(); // div id
	  } else {
	    $('#password2-error').text('Password has to be 9 or more characters, and contain at least 1 upper case, 1 lower case, and 1 number.').show();
	    event.preventDefault();  
            submit = false
	  }
    
    if(passwordsMatch(pwd, pwd_conf)){
    	$('#match-error').hide(); // div id
    } else {
    	$('#match-error').text('Your passwords do not match.').show();
    	event.preventDefault();
        submit = false
    }

    if( submit ){
        $.ajax({
            type: 'POST',
            url: '/users/registration/'
            contentType: 'application/json'
	    data: JSON.stringify({
		password: pwd,
		password_confirm: pwd_conf,
		age: age,
		email: email,
		firstname: firstname,
		lastname: lastname
            }),
	    dataType: 'json'
         }).done(function() {
		showAlert('Created the user!', 'success');
	 }).fail(function() {
		showAlert('Something went wrong', 'danger');
         });
     }
  });
});

