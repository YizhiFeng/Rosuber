var rh = rh || {};
rh.rb = rh.rb || {};

rh.rb.mdlInitializations = function() {
  // Polyfill for browsers that don't support the dialog tag.
  var dialogs = document.querySelectorAll('dialog');
  for (var i = 0; i < dialogs.length; i++) {
    // Using an old school style for loop since this for compatibility.
    var dialog = dialogs[i];
    if (!dialog.showModal) {
      dialogPolyfill.registerDialog(dialog);
    }
  }
};

rh.rb.enableButtons = function() { 
   
   $("#login-btn").click(function() {
    const registryToken = "de1ce252-8d67-48ba-b6c4-18fa74eeb67a";
   	Rosefire.signIn(registryToken, function(error, rosefireUser){
   		if(error){
   		 	console.log("Error communicating with Rosefire",error)
   		 	return;
   		}
   		window.location.replace("/rosefire-login?token="+ rosefireUser.token);
   	});
   });
   
    $("#logout-btn").click(function() {
	   document.querySelector("#logout-confirm-dialog").showModal();
   });
   
    $("#logout-btn-link").click(function() {
	   document.querySelector("#logout-confirm-dialog").showModal();
   });
   
   	$("#find-trip-link").click(function() {
 		document.querySelector('#find-trip-dialog').showModal();
 	});
 	
 	$("#add-trip-btn").click(function() {
 		document.querySelector('#add-trip-dialog').showModal();
 	});
   
    $("#delete-trip-btn").click(function() {
 		document.querySelector('#delete-trip-dialog').showModal();
 		var entity_key = $(this).find(".trip-entity-key-for-delete").html();
 		$("input[name=trip_to_delete_key]").val(entity_key)
 	});
   
    $("#signout-btn").click(function() {
    window.location.replace("/rosefire-logout");
  });
    
 // Cancel button on the delete confirmation dialog.
	$('.close-logout-confirm-dialog').click(function() {
		document.querySelector('#logout-confirm-dialog').close();
	});
	
	$('.close-add-trip-dialog').click(function() {
		document.querySelector('#add-trip-dialog').close();
	});
 	

 	$('.close-find-trip-dialog').click(function() {
		document.querySelector('#find-trip-dialog').close();
	});
 	
 	$("#driver-btn").click(function() {		
 		document.querySelector('#find-trip-dialog').close();
 	});
 	
 	$("#passenger-btn").click(function() {
 		document.querySelector('#find-trip-dialog').close();
 	});
 	
 	$(".close-delete-trip-dialog").click(function() {
 		document.querySelector('#delete-trip-dialog').close();
 	});
 	
 	
};


$(document).ready(function() {
  rh.rb.mdlInitializations();
  rh.rb.enableButtons();
});
