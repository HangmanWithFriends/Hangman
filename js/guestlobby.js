$(function() {
	    
	$('#request-guest-game').on('submit', function(event) {
		
		var $here = $(this);
		var $waitplace = $here.find('.wait-for-game');
		$waitplace.empty()
		$waitplace.append(
			$('<div>')
				.text("Waiting for a game")
		)

    });
});
