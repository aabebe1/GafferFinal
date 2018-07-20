$(document).ready(function() {
	var arrowSelected = false;
	
	$("#arrowContainer").click(function(event) {
		if (arrowSelected) {
			arrowSelected = false;
			$("#arrowContainer").css("background-color", "#53ea78");
		}
		else {
			arrowSelected = true;
			$("#arrowContainer").css("background-color", "#13a058");
		}
	});
	
	$("#sidePanel").mousedown(function(event) {
		if (event.target.id != "arrowImg") {
			arrowSelected = false;
			$("#arrowContainer").css("background-color", "#53ea78");
		}
	});
	
	$('.new-item').draggable({
		containment: ".drillSpace",
		helper: "clone",
		stack: ".new-item",
		revert: "invalid"
	});
	
	$("#drillBox").droppable({
		accept: ".tool",
		drop: dropHandler,
	});
	
	function dropHandler(event, ui) {
		var newPosX = ui.offset.left - $(this).offset().left;
		var newPosY = ui.offset.top - $(this).offset().top;

		clone = $(ui.helper).clone();
						
		if (clone.hasClass("new-item")) {
			clone.removeClass("new-item");
			clone.css({"left":newPosX,"top":newPosY});
			clone.draggable({
				containment: ".drillSpace",
				revert: function(valid) { if(!valid) {this.remove();} }
			});
			if (clone.hasClass("label")) {
				clone.attr("contenteditable", "true");
			}
	
			if (clone.hasClass("resizable")) {
				clone.children().rotatable();
			}
			// add item to field
			$(this).append(clone);
			$("#submitButton").prop('disabled', true);
			$("#message").html("<em>*Please save your image first</em>");
		}
	};
	
	var myCanvas = document.getElementById("drillCanvas");	
	var myTempCanvas = document.getElementById("tempCanvas");
	var context = myCanvas.getContext('2d');
	var tempContext = myTempCanvas.getContext('2d');
	tempContext.strokeStyle="rgba(0,0,0,.5)"
	var drawing = false;
	var startPos = {x:0, y:0};
	var endPos = {x:0, y:0};
	var canvasOffset = $("#drillCanvas").offset();
	var headlen = 8;
	
	function drawArrow(cntxt) {
		var angle = Math.atan2(endPos.y - startPos.y, endPos.x - startPos.x);

		cntxt.beginPath();
		cntxt.moveTo(startPos.x, startPos.y);
		cntxt.lineTo(endPos.x, endPos.y);	
		cntxt.lineTo(endPos.x-headlen*Math.cos(angle-Math.PI/6),endPos.y-headlen*Math.sin(angle-Math.PI/6));
		cntxt.moveTo(endPos.x, endPos.y);
		cntxt.lineTo(endPos.x-headlen*Math.cos(angle+Math.PI/6),endPos.y-headlen*Math.sin(angle+Math.PI/6));
		
		cntxt.stroke();				
	}
	
	function clearCanvas(cnvs, cntxt) {
		cntxt.clearRect(0, 0, cnvs.width, cnvs.height);
	}
	
	$("#tempCanvas").on("touchmove mousemove", function(event) {
		if (drawing === true) {
			event.preventDefault();
			endPos = {x: event.pageX - canvasOffset.left, y: event.pageY - canvasOffset.top};
			clearCanvas(myTempCanvas, tempContext);
			drawArrow(tempContext);
		}	
	});
	
	$("#tempCanvas").on("touchstart mousedown", function(event) {
		if (arrowSelected == true) {
	        blockMenuHeaderScroll = true;
			drawing = true;
			startPos = {x: event.pageX - canvasOffset.left, y: event.pageY - canvasOffset.top};
			endPos = {x: event.pageX - canvasOffset.left, y: event.pageY - canvasOffset.top};
		}
	});
	
	$(window).on("touchend mouseup", function() {
		if (drawing === true) {
			blockMenuHeaderScroll = false;
			clearCanvas(myTempCanvas, tempContext);
			drawArrow(context);
			startPos = {x:0, y:0};
			endPos = {x:0, y:0};	
			drawing = false;
		
			$("#submitButton").prop('disabled', true);
			$("#message").html("<em>*Please save your image first</em>");
		}
	});
	
	/* Saves drill Image */
	$("#saveButton").click(function(event) {
		html2canvas($("#drillBox"), {
			onrendered: function(canvas) {
				image_data = canvas.toDataURL("image/jpeg");
				$("#id_drillImage").val(image_data);
			}
		});	
		$("#submitButton").prop('disabled', false); /* allow user to submit */
		$("#message").html("");
	});
	
	$("#clearButton").click(function(event) {
		clearCanvas(myCanvas, context)
	});
	
});