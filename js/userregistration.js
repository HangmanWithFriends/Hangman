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


  $('#register-form').on('submit', function(event) { // form id
	  
	event.preventDefault();

	var name = $('#user-name-input').val(); // input id
  var email = $('#user-email-input').val(); // input id
  var pwd = $('#user-password-input').val(); // input id
  var pwd_confirm = $('#user-password-confirm-input').val();
  var post = true;
  
  document.getElementById("errorbox").style.color = "Red";

  if(!isValidEmail(email)) {
    $('#user-email-input').val('')
    document.register.usermail.focus()
    document.getElementById("errorbox").innerHTML = "Email must be in the correct format."
    event.preventDefault();
    post = false;
  }

  if(!isValidPassword(pwd)) {
    $('#user-password-input').val('')
    $('#user-password-confirm-input').val('')
    document.register.password.focus()
    document.getElementById("errorbox").innerHTML = "Password has to be 7 or more characters, and contain at least 1 number, and 1 letter."
    event.preventDefault();
    post = false;
  }

  if(!isPasswordMatch(pwd, pwd_confirm)) {
    $('#user-password-input').val('');
    $('#user-password-confirm-input').val('');
    document.register.password.focus();
    document.getElementById("errorbox").innerHTML = "Passwords don't match";
    event.preventDefault();
    post = false;
  }

  if(post){
    $.ajax({
          type : 'POST',
          url: '/register',
          contentType: 'application/json',
          data: JSON.stringify({
              usermail: email,
              password: pwd,
              username: name
          }),
          dataType: 'json'
      }).done(function(data) {
          console.log('done posting');
          var d = data;
          if(d.errors.length > 0){
            document.getElementById("errorbox").innerHTML = "Registration unsuccessful";
          }
          else{
            var uid = d.result;
            window.location.href = "/lobby/" + uid;
          } 
      }).fail(function() {
          document.getElementById("errorbox").innerHTML = "Registration unsuccessful";
      });
  }

});
});

