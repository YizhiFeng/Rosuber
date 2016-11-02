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

rh.rb.createTripInit = function() {
	 // Initialize the date picker widget.
  $('input[name=pick_up_time]').bootstrapMaterialDatePicker({
    format : 'MM-DD-YYYY hh:mm A',
  });
  
  $(".scheduled-picker").show();
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
   
    $(".delete-trip-btn").click(function() {
 		document.querySelector("#delete-trip-dialog").showModal();
 		var entity_key = $(this).find(".trip-entity-key-for-delete").html();
 		$("input[name=trip_to_delete_key]").val(entity_key)
 	});
   
   
    $("#signout-btn").click(function() {
    window.location.replace("/rosefire-logout");
    });
    
    $("#add-trip-btn").click(function() {
    	window.location.replace("/new-trip");
     });
    
    $("#find-trip-link").click(function() {
        $("#add_new_trip_button").removeClass("hidden");
      });
    
    $("input[name=role_radio_group]").change(function() {
 		if(this.id == "passenger-radio"){
 			$("#capacity-field").addClass("hidden");
 		}
 	});
    
    
    
 // Cancel button on the delete confirmation dialog.
	$('.close-logout-confirm-dialog').click(function() {
		document.querySelector('#logout-confirm-dialog').close();
	});
	
	$('.close-add-trip-dialog').click(function() {
		window.location.replace("/find-trip");
	});

 	$(".close-delete-trip-dialog").click(function() {
 		document.querySelector('#delete-trip-dialog').close();
 	});
 	
 	$(".close-update-trip-dialog").click(function() {
 		document.querySelector('#update-trip-dialog').close();
 	});
 	
 	
};


$(document).ready(function() {
  rh.rb.mdlInitializations();
  rh.rb.enableButtons();
  rh.rb.createTripInit();
});
