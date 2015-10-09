var uid_element = document.getElementById("uid");
var gid_element = document.getElementById("gid");
var uid = uid_element.innerHTML;
var gid = gid_element.innerHTML;
var myInterval = 0;
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
		var djson = JSON.parse(data);
        right_letters = djson.correct_letters;
        wrong_letters = djson.incorrect_letters;
        wrong_phrases = djson.incorrect_words;
        var win_uid = djson.win;
        var guess_uid = djson.guesser_uid;
        var creator_uid = djson.creator_uid;
 
        var message = "";

        if(win_uid == uid){
            if(uid == guess_uid){
                message = "You correctly guessed the phrase!";
            }
            else{
                message = "Your opponent failed to guess your word!";
            }
            clearInterval(myInterval);
            window.alert(message);
            window.location.href = "/guestlobby/"+uid;
        }
        else if(win_uid == guess_uid){
            message = "Your opponent got loose from the noose. You lose!";
	        clearInterval(myInterval);
            window.alert(message);
            window.location.href = "/guestlobby/"+uid;
        }
        else if(win_uid == creator_uid){
            message = "You died.";
	        clearInterval(myInterval);
            window.alert(message);
            window.location.href = "/guestlobby/"+uid;  
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
		var djson = JSON.parse(data);
        new_right_letters = djson.correct_letters;
        new_wrong_letters = djson.incorrect_letters;
        new_wrong_phrases = djson.incorrect_words;
    });

    if(new_right_letters.length != right_letters.length){
    	window.location.href="/gameplay/" + uid + "/" + gid;
    }
    if(new_wrong_letters.length != wrong_letters.length){
    	window.location.href="/gameplay/" + uid + "/" + gid;
    }
    if(new_wrong_phrases.length != wrong_phrases.legnth){
    	window.location.href="/gameplay/" + uid + "/" + gid;
    }
        
}
