// Copyright (c) 2023, VV SYSTEMS DEVELOPER LTD and contributors
// For license information, please see license.txt

frappe.ui.form.on('Truck', {
	// refresh: function(frm) {

	// }
	setup: function(frm){
		frm.set_query('trans_ms_driver', function () {
			return{
				filters: {
					"status": "Active"
				}
			}
			
		})
	},
	onload: function (frm) {
		// Select the element with data-fieldname="disabled"
		const element = document.querySelector('[data-fieldname="disabled"]');

		// Set its style color to red
		element.style.color = "red";

		frappe.db.get_single_value("Transport Settings", "vehicle_fuel_parent_warehouse")
		.then(function(value) {
			var default_parent_warehouse = value;

			frm.set_query("trans_ms_fuel_warehouse", function () {
				return {
					"filters": {
						"parent_warehouse": default_parent_warehouse
					}
				};
			});
		})
	},
	trans_ms_maintain_stock: (frm) => {
		frm.doc.trans_ms_fuel_warehouse = "";

	},
	refresh: function(frm){
		if (frm.doc.status != "On Trip"){
			frm.doc.trans_ms_current_trip = ''
			frm.refresh_field("trans_ms_current_trip")
		}
	},


	license_plate: (frm) =>{
		//check for lenght and format...
		//ld0101ld\

		if (cur_frm.doc.license_plate.length == 4 && cur_frm.doc.license_plate == "0000"){
			//Case 0000 only means has no PLATE YET; veiculo_numero_chassi is required
			cur_frm.get_field('veiculo_numero_chassi').df.reqd = true
			cur_frm.refresh_fields('veiculo_numero_chassi');

		} else if (cur_frm.doc.license_plate.length < 7 ){
			// lda-01-02
			frappe.show_alert('license_plate tem que ter 11,9,8 ou 7 caracteres e digitos');
		} else if (cur_frm.doc.license_plate.length < 8 ){
			frappe.show_alert('license_plate tem que ter 11,9 ou 8 caracteres e digitos');
		} else if (cur_frm.doc.license_plate.length < 11 && cur_frm.doc.license_plate.length != 8 && cur_frm.doc.license_plate.length != 9 && cur_frm.doc.license_plate.length != 10){
			frappe.show_alert('license_plate tem que ter 11,9 ou 8 caracteres e digitos');
		}
		//format the plate
		console.log('plates');
		console.log(cur_frm.doc.license_plate.replace(/[^0-9]/g,"").length);
		console.log(cur_frm.doc.license_plate.length);
		//FIX 03-06-2024; Case plates is 10 chars..ex abc0102abc
		if (cur_frm.doc.license_plate.length == 9 || cur_frm.doc.license_plate.length == 10 ){
			//assuming 3 fist as Letters
			if (isNaN(cur_frm.doc.license_plate.substr(0,3))) {
				//Correcto nao sao Numero os 3 primeiros digitos
				var tmp_plate = "";
				//FIX 03-06-2024
				var x = 0;
				while (x < cur_frm.doc.license_plate.length) {
					if (x == 2 || x == 4 || x == 6 ){
						tmp_plate += cur_frm.doc.license_plate[x] + "-";

					} else {
						tmp_plate += cur_frm.doc.license_plate[x];
					}
					
					x++;
				}
				cur_frm.doc.license_plate = tmp_plate.toUpperCase();
				cur_frm.refresh_fields('license_plate');


			} else {
				frappe.show_alert('license_plate tem que ter 11,10,9 ou 8 caracteres e digitos');
			}

		} else if (cur_frm.doc.license_plate.length == 8 ){
			var tmp_plate = "";
			for (var x in cur_frm.doc.license_plate) {
				//case 123-xx-123
				//FIX 06-12-2023; Fix when tmp_plate is completed... 
				if (tmp_plate.length == 11){
					break;
				} else if ((tmp_plate.match(/-/g) || []).length == 2) {
					//FIX 18-01-2024; Has the 2 - so can break.
					if (tmp_plate.length == 10){
						break;
					}
				}


				if (cur_frm.doc.license_plate.replace(/[^0-9]/g,"").length == 6 && cur_frm.doc.license_plate.replace(/[^a-zA-Z]/g,"").length == 2) {
					if (isNaN(cur_frm.doc.license_plate.substr(3,2)) == true){
						//123-CD-123
						if (x == 2){
							tmp_plate += cur_frm.doc.license_plate[x] + "-";
						} else if (x == 4){
							tmp_plate += cur_frm.doc.license_plate[x] + "-";

						} else {
							tmp_plate += cur_frm.doc.license_plate[x];
						}
					}

				} else if (x == 1 || x == 3 || x == 5 ){
					tmp_plate += cur_frm.doc.license_plate[x] + "-";

				} else {
					tmp_plate += cur_frm.doc.license_plate[x];
				}

			}
			cur_frm.doc.license_plate = tmp_plate.toUpperCase();
			cur_frm.refresh_fields('license_plate');

		} else if (cur_frm.doc.license_plate.length == 7 ){
			var tmp_plate = "";
			for (var x in cur_frm.doc.license_plate) {
				//FIX 06-12-2023; Fix when tmp_plate is completed... 
				if (tmp_plate.length == 11){
					break;
				} else if ((tmp_plate.match(/-/g) || []).length == 2) {
					//FIX 18-01-2024; Has the 2 - so can break.
					if (tmp_plate.length == 9){
						break;
					}
				}

				//Special CD-123-12 e 123-CD-12
				if (cur_frm.doc.license_plate.replace(/[^0-9]/g,"").length == 5 && cur_frm.doc.license_plate.replace(/[^a-zA-Z]/g,"").length == 2) {
					console.log('especial');
					//Check if first is lettters or numbers
					console.log(isNaN(cur_frm.doc.license_plate.substr(3,2)));
					if (isNaN(cur_frm.doc.license_plate.substr(3,2)) == true){
						//123-CD-12
						if (x == 2){
							tmp_plate += cur_frm.doc.license_plate[x] + "-";
						} else if (x == 4){
							tmp_plate += cur_frm.doc.license_plate[x] + "-";

						} else {
							tmp_plate += cur_frm.doc.license_plate[x];
						}

					} else {
						if (x == 1){
							tmp_plate += cur_frm.doc.license_plate[x] + "-";
						} else if (x == 4){
							tmp_plate += cur_frm.doc.license_plate[x] + "-";

						} else {
							tmp_plate += cur_frm.doc.license_plate[x];
						}

					}

				} else if (x == 2 || x == 4 ){
					tmp_plate += cur_frm.doc.license_plate[x] + "-";

				} else {
					tmp_plate += cur_frm.doc.license_plate[x];
				}

			}
			cur_frm.doc.license_plate = tmp_plate.toUpperCase();
			cur_frm.refresh_fields('license_plate');

		}else if (cur_frm.doc.license_plate.length == 11 ){
			console.log('Nao faz nada...esta certo');
		}
	}


	
});
