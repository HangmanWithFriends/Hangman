$(function() {
	var $uid = document.getElementById("var-uid").getAttribute('value');
	var $gid = document.getElementById("var-gid").getAttribute('value');
	
	
	setTimeout(function(){
		window.location.href="/gameplay/" + $uid + "/" + $gid;
//		$.ajax({
//			type : 'GET',
//			url : '/game/' + $gid
//		}).done(function(data) {
//			var d = data;
//			d_json = JSON.parse(d);
//			var wrong_letters = d_json.incorrect_letters;
//			console.log(wrong_letters);
//			var wl;
//			for(wl in wrong_letters){
//				console.log(wrong_letters[wl]);
//				var wrongspot = document.getElementsByClassName('wrong ' + wl);
//				console.log(wrongspot);
//			}
//			var a = document.getElementsByClassName('A');
//			console.log(a);
//			a.addClass('wrong')
//		});
		
	}, 1000);
});
