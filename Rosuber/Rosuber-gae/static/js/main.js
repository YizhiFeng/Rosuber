$(document).ready(function() {
       
   
   
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
});