var json = document.getElementById("data");
var config = JSON.parse(json.textContent);

function getTrackingInfo(successCallback, failureCallback) {
	$.ajax({
		url: "/tracking/pin/verify/",
		method: "POST",
		data: config,
		success: successCallback,
		error: failureCallback	
	});
}

function verifyPIN() {
	var pin = $("#pinText").val()
	console.log(pin);

	config.pin = pin;
	getTrackingInfo(verifyPinSuccess, verifyPinFailure);
}

function verifyPinSuccess(data, status, req) {
	console.log(data);
	var coords = data.location.split(",");
	var mapCanvas = document.getElementById('map');
	var latlng = new google.maps.LatLng(coords[0], coords[1]);

	var map = new google.maps.Map(mapCanvas, {
		center: latlng,
		zoom: 15,
		mapTypeId: google.maps.MapTypeId.ROADMAP
	});

	var marker = new google.maps.Marker({
		position: latlng,
		map: map,
		title: data.first_name + " " + data.last_name 
	});

	$("#info").text(JSON.stringify(data));
	hideModal();
}

function verifyPinFailure(req, status, err) {

}

function showModal() {
	$("#pinModal").modal({
		keyboard: false,
		backdrop: "static"
	});
}

function hideModal() {
	$("#pinModal").modal("hide");
}