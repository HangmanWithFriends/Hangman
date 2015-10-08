$(function() {
    var uid_element = document.getElementById("uid");
    var gid_element = document.getElementById("gid");

    var uid = uid_element.innerHTML;//$('#uid').val();
    var gid = gid_element.innerHTML;//$('#gid').val();

    $.ajax({
        type : 'GET',
        url : '/game/'+ gid,
        contentType: 'application/json',
    }).done(function(data){
        console.log("before vars");

        console.log(gid);
        console.log(uid);


        var djson = JSON.parse(data);
        console.log("after vars 2");
        var win_uid = djson.win;
        console.log("after vars 3");

        var guess_uid = djson.guesser_uid;
        console.log("after vars 4");

        var creator_uid = djson.creator_uid;
        console.log("after vars 5");

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
            message = "Your opponent correctly guessed your phrase.";
            window.alert(message);
            window.location.href = "/guestlobby/"+uid;
        }
        else if(win_uid == creator_uid){
            message = "You failed ot guess your opponent's phrase.";
            window.alert(message);
            window.location.href = "/guestlobby/"+uid;
        }
    })
});

