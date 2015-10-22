var uid_element = document.getElementById("uid");
var gid_element = document.getElementById("gid");
var uid = uid_element.innerHTML;
var gid = gid_element.innerHTML;
var myInterval = 0;
var old_djson = null
var new_djson = null
var right_letters = [];
var wrong_letters = [];
var wrong_phrases = [];
var new_right_letters = [];
var new_wrong_letters = [];
var new_wrong_phrases = [];

$.ajax({
        type : 'GET',
        url : '/game/'+ gid,
        contentType: 'application/json',
	}).done(function(data) {
		old_djson = JSON.parse(data);
        var win_uid = old_djson.win;
        var guess_uid = old_djson.guesser_uid;
        var creator_uid = old_djson.creator_uid;
        var message = "";
        var redirect_location = "/lobby/" + uid;

        if(uid.charAt(0) == 'g')
        {
            var redirect_location = "/guestlobby/"+uid;
        } 
        
        if(win_uid == uid){
            if(uid == guess_uid){
                message = "You correctly guessed the phrase!";
            }
            else{
                message = "Your opponent failed to guess your word!";
            }
            window.alert(message);
            window.location.href = redirect_location; 
        }
        else if(win_uid == guess_uid){
            message = "Your opponent got loose from noose. You lose!";
            window.alert(message);
            window.location.href = redirect_location;
        }
        else if(win_uid == creator_uid){
            message = "You died.";
            window.alert(message);
            window.location.href = redirect_location;
        }
        else{
            myInterval = setInterval(function(){ poll_updates(); }, 3000);
        }
});

function poll_updates(){
    $.ajax({
        type : 'GET',
        url : '/game/'+ gid,
        contentType: 'application/json',
	}).done(function(data) {
        console.log("in done");
		new_djson = JSON.parse(data);


        console.log(new_djson.correct_letters)
        console.log(old_djson.correct_letters)

        console.log(new_djson.incorrect_letters)
        console.log(old_djson.incorrect_letters)

        console.log(new_djson.incorrect_words)
        console.log(old_djson.incorrect_words)

        if(new_djson.correct_letters.length != old_djson.correct_letters.length){
            console.log('correct_letters\n')

            window.location.href="/gameplay/" + uid + "/" + gid;
        }
        if(new_djson.incorrect_letters.length != old_djson.incorrect_letters.length){
            console.log('incorrect_letters\n')


            window.location.href="/gameplay/" + uid + "/" + gid;
        }
        if(new_djson.incorrect_words.length != old_djson.incorrect_words.length){
            console.log('incorrect_words\n')

            window.location.href="/gameplay/" + uid + "/" + gid;
        }
    });        
}
