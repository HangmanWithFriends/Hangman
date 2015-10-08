$(function() {
    $(document).ready({
        $.ajax({
            type : 'GET',
            url : '/game/'+uid+'/'+gid,
            contentType: 'application/json',
        }).done(function(data){
            var d = data;
            var dict = json.parse(d);
            var win_uid = dict['win']
            var guess_uid = dict['guesser_uid']
            var creator_uid = dict['creator_uid']
            var message = ""
            var display = true;
            if(win_uid == uid){
                if(uid == guess_uid){
                    message = "You correctly guessed the phrase!";
                }
                else{
                    message = "Your opponent failed to guess your word!"
                }
            }
            else if(win_uid == guess_uid){
                message = "Your opponent correctly guessed your phrase.";
            }
            else if(win_uid == creator_uid){
                message = "You failed ot guess your opponent's phrase."
            }
            else{
                display = false;
            }
            
            if(display){
                window.alert(message)
                                
				window.location.href = "/guestlobby/"+uid;
            }
        })
    });

	$('#guess-form').on('submit', function(event) {
		
		event.preventDefault();

		var guess = $('#guess-input').val();
        var uid = $('#page-uid').val();
        var gid = $('#page-gid').val();
		}
		
		/* Send the data to 'POST /users/login' to see if this username/password works */
		$.ajax({
			type : 'POST',
			url: '/game/'+uid+"/"+gid,
			contentType: 'application/json',
			data: JSON.stringify({
				guessed: guess
			}),
			dataType: 'json'
		}).done(function(data) {
			var d = data;
			if(d.errors.length > 0){
			}
            else{
               location.reload(); 
			}
			
		}).fail(function() {
        });
});

