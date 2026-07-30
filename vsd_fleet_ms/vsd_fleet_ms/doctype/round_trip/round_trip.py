# Copyright (c) 2023, VV SYSTEMS DEVELOPER LTD and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class RoundTrip(Document):
	def after_insert(self):
		#TO BE REMOVED...
		print ('After insert....')
		for trips in self.trip_details:
			trip = frappe.get_doc("Trips",trips.trip_id)
			if trip.round_trip != self.name:
				trip.round_trip = self.name
				trip.save()

	def before_save(self):
		self.sync_trip_links()

	def sync_trip_links(self):
		current_trip_ids = {row.trip_id for row in (self.trip_details or []) if row.trip_id}
		existing_trip_ids = set(
			frappe.get_all("Trips", filters={"round_trip": self.name}, pluck="name")
		)

		print ('Sync trip links...')
		print ('current ', current_trip_ids)
		print ('existing ', existing_trip_ids)

		print (self.status)
		print (self.docstatus)

		print ('Isnew ', self.is_new())

		if self.docstatus == 1:
			for trip_id in existing_trip_ids - current_trip_ids:
				trip = frappe.get_doc("Trips", trip_id)
				if trip.round_trip:
					trip.round_trip = ""
					trip.save()

			for trip_id in current_trip_ids:
				trip = frappe.get_doc("Trips", trip_id)
				print ('self.name ',self.name)
				if trip.round_trip != self.name:
					trip.round_trip = self.name
					trip.save()
