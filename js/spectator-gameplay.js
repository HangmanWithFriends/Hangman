var myInterval = setInterval(function(){ window.location.href = poll_updates(); }, 1000);

function poll_updates(){
    var uid_element = document.getElementById("uid");
    var gid_element = document.getElementById("gid");

    var uid = uid_element.innerHTML;
    var gid = gid_element.innerHTML;
    console.log(gid);
    $.ajax({
        type : 'GET',
        url : '/game/'+ gid,
        contentType: 'application/json',
	}).done(function(data) {
		var d_json = JSON.parse(data);
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
    })

	window.location.href="/gameplay/" + uid + "/" + gid;
}
