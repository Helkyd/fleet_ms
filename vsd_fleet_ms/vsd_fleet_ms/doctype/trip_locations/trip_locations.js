// Copyright (c) 2023, VV SYSTEMS DEVELOPER LTD and contributors
// For license information, please see license.txt

//Last Modified: 07-07-2026

frappe.ui.form.on('Trip Locations', {
	// refresh: function(frm) {

	// }
	latitude(frm) {
		console.log('Lat ', frm);
		geolocation(frm);
	},
	longitude(frm) {
		console.log('Long ', frm);
		geolocation(frm);
	},
	onload_post_render(frm) {
		console.log('Geo... ', frm);
		geolocation(frm);
	}

});
function geolocation(frm){
	//FIX 07-07-2026; Changed == 0 to != 0
	if (frm.doc.latitude != 0 && frm.doc.longitude != 0) {
		console.log('geo lat e long.....')
		console.log('lat ', frm.doc.latitude)
		console.log('long ', frm.doc.longitude)
		frm.fields_dict.location_latitude_longitude.map.setView([frm.doc.latitude, frm.doc.longitude], 13);
	}
	else {
			frm.doc.latitude = frm.fields_dict.location_latitude_longitude.map.getCenter()['lat'];
			frm.doc.longitude = frm.fields_dict.location_latitude_longitude.map.getCenter()['lng'];
	}
}
