$(function() {
    var uid_element = document.getElementById("uid");
    var gid_element = document.getElementById("gid");

    var uid = uid_element.innerHTML;
    var gid = gid_element.innerHTML;

    $.ajax({
        type : 'GET',
        url : '/game/'+ gid,
        contentType: 'application/json',
    }).done(function(data){
        var djson = JSON.parse(data);
        var win_uid = djson.win;
        var guess_uid = djson.guesser_uid;
        var creator_uid = djson.creator_uid;
        var answer = djson.answer;
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
            message = "Oh no! You died. The word was " + answer;
            console.log(answer)
            window.alert(message);
            window.location.href = redirect_location;
        }
    });
});

var letterGlobal;

function sendLetter(letter) {
    console.log(letter);
    
}

function setLG(toSet) {
    letterGlobal = toSet;
}

function getLG() {
    return letterGlobal;
}
