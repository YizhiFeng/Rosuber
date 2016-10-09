/** namespace. */
var rh = rh || {};
rh.mq = rh.mq || {};

rh.mq.editing = false;

rh.mq.attachEventHandlers = function() {
	$('#insert-quote-modal').on('shown.bs.modal', function() {
		$("input[name='quote']").focus();
	});
};

rh.mq.hideNavbar = function() {
	var $navbar = $(".navbar-collapse");
	if($navbar.hasClass("in")){
		$navbar.collapse("hide");
	}
}

rh.mq.enableButtons = function() {

	// Attach a click listener to the edit button.
	$("#toggle-edit-mode").click(function() {
		if (rh.mq.editing) {
			rh.mq.editing = false;
			$(".edit-actions").addClass("hidden");
			$(this).html("Edit");
		} else {
			rh.mq.editing = true;
			$(".edit-actions").removeClass("hidden");
			$(this).html("Done");
		}
		rh.mq.hideNavbar();
	});

	$("#add-movie-quote").click(
			function() {
				$("#insert-quote-modal .modal-title").html("Add a MoviQuote");
				$("#insert-quote-modal button[type=submit]").html("Add Quote");

				$("#insert-quote-modal input[name=quote]").val("");
				$("#insert-quote-modal input[name=movie]").val("");
				$("#insert-quote-modal input[name=entity_key]").val("").prop(
						"disabled", true);
				rh.mq.hideNavbar();
			});

	$(".edit-movie-quote").click(
			function() {
				$("#insert-quote-modal .modal-title").html(
						"Edit this MoviQuote");
				$("#insert-quote-modal button[type=submit]").html(
						"Update Quote");

				var quote = $(this).find(".quote").html();
				var movie = $(this).find(".movie").html();
				var entityKey = $(this).find(".entity-key").html();
				$("#insert-quote-modal input[name=quote]").val(quote);
				$("#insert-quote-modal input[name=movie]").val(movie);
				$("#insert-quote-modal input[name=entity_key]").val(entityKey)
						.prop("disabled", false);
				rh.mq.hideNavbar();
			});

	$(".delete-movie-quote").click(function() {
		var entityKey= $(this).find(".entity-key").html();
		$("#delete-quote-modal input[name=entity_key]").val(entityKey);
	});
};

$(document).ready(function() {
	rh.mq.enableButtons();
	rh.mq.attachEventHandlers();
});