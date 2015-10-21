$(function() {
  function isValidEmail(email) {
    // var re = /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/;
	  var re = /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9_.+-]+.[a-zA-Z0-9_.+-]+$/;
    console.log("in valid email")
    console.log(re.test(email))
    return re.test(email);
  }

  function isValidPassword(pwd) {
    // at least one number, one letter
    // at least nine characters
    var re = /(?=.*\d)(?=.*[a-zA-z]).{7,}/;
    console.log("in valid password")
    console.log(re.test(pwd))
    return re.test(pwd);
  }

  function isPasswordMatch(pwd, pwd_confirm) {
    console.log("in password match")
    console.log(pwd == pwd_confirm )
    return pwd == pwd_confirm    
  }


  $('#settings-form').on('submit', function(event) { // form id
	  
	event.preventDefault();

	var name = $('#user-name-input').val(); // input id
  	var email = $('#user-email-input').val(); // input id
  	var pwd = $('#user-password-input').val(); // input id
	var new_pwd = $('#user-new-password-input').val(); // input id
  	var new_pwd_confirm = $('#user-new-password-confirm-input').val();
	var uid = $('#uid').text();
	var old_email = $('#old_email').text();
  	var post = true;
  	console.log('Updating Settings');
	  console.log(uid);
  document.getElementById("errorbox").style.color = "Red";

  if(!isValidEmail(email)) {
    $('#user-email-input').val('')
    document.Settings.usermail.focus()
    document.getElementById("errorbox").innerHTML = "Email must be in the correct format."
    event.preventDefault();
    post = false;
  }

  if(!isValidPassword(new_pwd) && new_pwd.length !== 0) {
    $('#user-new-password-input').val('')
    $('#user-new-password-confirm-input').val('')
    document.Settings.newpassword.focus()
    document.getElementById("errorbox").innerHTML = "Password has to be 7 or more characters, and contain at least 1 number, and 1 letter."
    event.preventDefault();
    post = false;
  }

  if(!isPasswordMatch(new_pwd, new_pwd_confirm)) {
    $('#user-new-password-input').val('');
    $('#user-new-password-confirm-input').val('');
    document.Settings.newpassword.focus();
    document.getElementById("errorbox").innerHTML = "Passwords don't match";
    event.preventDefault();
    post = false;
  }

  if(post){
    $.ajax({
          type : 'POST',
          url: '/settings/'+ uid,
          contentType: 'application/json',
          data: JSON.stringify({
              usermail: email,
			  old_usermail: old_email,
              password: pwd,
			  newpassword: new_pwd,
              username: name
          }),
          dataType: 'json'
      }).done(function(data) {
          console.log('done posting');
          var d = data;
          if(d.errors.length > 0){
            var err_message = d.errors[0]
            console.log(err_message)
            document.getElementById("errorbox").innerHTML = err_message;
          }
         else{
            var uid = d.result;
            window.location.href = "/settings/" + uid;
          }
      }).fail(function() {
          document.getElementById("errorbox").innerHTML = "Updating Settings unsuccessful";
      });
  }

});
});

