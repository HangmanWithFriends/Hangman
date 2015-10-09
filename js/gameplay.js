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
        var message = "";

        if(win_uid == uid){
            if(uid == guess_uid){
                message = "You correctly guessed the phrase!";
            }
            else{
                message = "Your opponent failed to guess your word!";
            }
            window.alert(message);
            window.location.href = "/guestlobby/"+uid;
        }
        else if(win_uid == guess_uid){
            message = "Your opponent got loose from noose. You lose!";
            window.alert(message);
            window.location.href = "/guestlobby/"+uid;
        }
        else if(win_uid == creator_uid){
            message = "You died.";
            window.alert(message);
            window.location.href = "/guestlobby/"+uid;
        }
    })
});
