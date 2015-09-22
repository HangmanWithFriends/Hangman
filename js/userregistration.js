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
  $('#user-add-form').on('submit', function(event) { // form id

    var email = $('#user-email-input').val(); // input id
    var age = $('#user-age-input').val();	// input id
    var pwd = $('#user-password-input').val(); // input id
    var pwd_conf = $('#user-password-input-confirm').val(); // input id

    if(isValidEmail(email)) {
      $('#email-error').hide(); // div id
    } else {
      $('#email-error').text('Email must be in the correct format.').show();
      event.preventDefault();
    }

    if(isValidAge(age)){
    	$('#age-error').hide();
    } else {
    	$('#age-error').text('Age must contain only digits.').show();
    	event.preventDefault();
    }
    if(isValidPassword(pwd)) {
      $('#password1-error').hide(); // div id
    } else {
      $('#password1-error').text('Password has to be 9 or more characters, and contain at least 1 upper case, 1 lower case, 1 number, and 1 symbol.').show();
      event.preventDefault();
    }
    if(isValidPassword(pwd_conf)) {
	    $('#password2-error').hide(); // div id
	  } else {
	    $('#password2-error').text('Password has to be 9 or more characters, and contain at least 1 upper case, 1 lower case, 1 number, and 1 symbol.').show();
	    event.preventDefault();
	  }
    
    if(passwordsMatch(pwd, pwd_conf)){
    	$('#match-error').hide(); // div id
    } else {
    	$('#match-error').text('Your passwords do not match.').show();
    	event.preventDefault();
    }
    

  });
});

