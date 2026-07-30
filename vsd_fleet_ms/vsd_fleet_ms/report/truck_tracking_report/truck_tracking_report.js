// Copyright (c) 2026, VV SYSTEMS DEVELOPER LTD and contributors
// For license information, please see license.txt

frappe.query_reports["Truck Tracking Report"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"reqd": 1
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"reqd": 1
		},
		{
			"fieldname": "customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options": "Customer",
		},
		{
			"fieldname": "manifest",
			"label": __("Manifest"),
			"fieldtype": "Link",
			"options": "Manifest",
		},
		{
			"fieldname": "truck",
			"label": __("Truck"),
			"fieldtype": "Link",
			"options": "Truck",
		},
		{
			"fieldname": "driver",
			"label": __("Driver"),
			"fieldtype": "Link",
			"options": "Truck Driver",
		},
		{
			"fieldname": "transporter_type",
			"label": __("Transporter Type"),
			"fieldtype": "Select",
			"options": "\nIn House\nSub- Contractor",
		},
		{
			"fieldname": "main_route",
			"label": __("Main Route"),
			"fieldtype": "Link",
			"options": "Trip Routes",
		}
	]
};