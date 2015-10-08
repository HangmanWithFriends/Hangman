$(function() {

	var showAlert = function(message, type) {

	    /* This stuctured mess of code creates a Bootstrap-style alert box.
	     * Note the use of chainable jQuery methods. */
	    var $alert = (
	      $('<div>')                // create a <div> element
	        .text(message)          // set its text
	        .addClass('alert')      // add some CSS classes and attributes
	        .addClass('alert-' + type)
	        .addClass('alert-dismissible')
	        .attr('role', 'alert')
	        .prepend(               // prepend a close button to the inner HTML
	          $('<button>')         // create a <button> element
	            .attr('type', 'button') // and so on...
	            .addClass('close')
	            .attr('data-dismiss', 'alert')
	            .html('&times;')    // &times; is code for the x-symbol
	        )
	        .hide()  // initially hide the alert so it will slide into view
	    );
	    
	    /* Add the alert to the alert container. */
	    $('#alerts').append($alert);

	    /* Slide the alert into view with an animation. */
	    $alert.slideDown();
	  };
	    
	$('#guest-login').on('submit', function(event) {
		
		event.preventDefault();
		
		/* Send the data to 'GET /guestlobby' to receive a uid */
		$.ajax({
			type : 'GET',
			url: 'get-guest-uid'
		}).done(function(data) {
			var d = data;
			var actual_json = JSON.parse(d);
//			var uid = d.uid.toString();
			console.log(actual_json.uid);
			window.location.href = "/guestlobby/" + actual_json.uid;
			
		}).fail(function() {
			showAlert('Username/password combination is wrong.', 'danger');
		});

	    });
    });

