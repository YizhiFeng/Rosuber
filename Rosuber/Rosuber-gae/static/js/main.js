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
    var logoutUrl = $(this).find(".logout-url").html();
    window.location.replace(logoutUrl);
  });
  
    
};


$(document).ready(function() {
  rh.rb.mdlInitializations();
  rh.rb.enableButtons();
});
