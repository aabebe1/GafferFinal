$(document).ready(function() {
	var editing = false;
	
	$("#editButton").click(function (event) {
		editing = true;
		$(".planField").attr("disabled", false);
		$("#editButton").attr("disabled", true);
		$("#saveButton").attr("disabled", false);
		$("#typeField").focus();
		window.scrollTo(0, 0);
	});
	
	$("#saveButton").click(function (event) {
		editing = false;
		$(".planField").attr("disabled", true);
		$("#editButton").attr("disabled", false);
		$("#saveButton").attr("disabled", true);
		
		// save values to form
		$("#id_planId").val({{ plan_details.id }});
		$("#id_planType").val($("#typeField").val());
		$("#id_planDescription").val($("#descriptionField").val());
		$("#id_planNotes").val($("#notesField").val());
		$("#id_planDate").val($("#dateField").val());
	});
	
	window.onbeforeunload = function() {
		if (editing) {
			return "Do you want to leave before saving your changes?";
		}
	}
	
});