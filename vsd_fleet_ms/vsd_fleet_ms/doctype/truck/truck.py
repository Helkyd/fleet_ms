# Copyright (c) 2023, VV SYSTEMS DEVELOPER LTD and contributors
# For license information, please see license.txt

#Last Modified: 21-03-2026
import frappe
from frappe.model.document import Document
import time

class Truck(Document):
	def before_save(self):
		current_status = frappe.db.get_value("Truck",self.name,"status")

		if current_status:
			if current_status != self.status:
				if self.status == "On Trip":
					doc = frappe.new_doc("Truck Log")
					doc.truck = self.name
					doc.vehicle_status = self.status
					doc.current_trip = self.trans_ms_current_trip 
					doc.save()
				else:
					doc = frappe.new_doc("Truck Log")
					doc.truck = self.name
					doc.vehicle_status = self.status
					doc.save()
    
		if not self.truck_number:
			self.truck_number = self.license_plate
		if self.disabled == 1:
			# Query Vehicle Trips Doctype for the given truck
			vehicle_trip = frappe.get_all("Trips", filters={"truck": self.name, "trip_completed": 0})

			
			if vehicle_trip:
            
				trip_doctype = "Trips"
				trip_name = vehicle_trip[0].name
			
				if trip_doctype and trip_name:
					doc_link = frappe.utils.get_link_to_form(trip_doctype, trip_name)
					
					frappe.throw(f"Trip found for this truck. Please complete the trip to be able to disable this vehicle: {doc_link}")

			else:
				self.status = "Disabled"
		if self.status == "Disabled":
			self.disabled == 1

	def on_update(self):
		#FIX 21-03-2026; Check if Officinas app installed
		print ('on update truck... ', self.license_plate)
		print ('Apps installed ', frappe.get_installed_apps())
		print ("aoerp_oficinas" in frappe.get_installed_apps())
		if "aoerp_oficinas" in frappe.get_installed_apps():
			camiao = frappe.get_list('Veiculos',fields=['name'],filters=[['name','=',self.license_plate]])
			if camiao == []:
				print ('Truck does not existe.... creating...')
				modelo_camiao = frappe.get_list('Marca Carros',fields=['name','modelo'],filters=[['modelo','=',self.model]])
				if modelo_camiao == []:
					print ('Create Model and Make for Trucks...')
					modelo_camiao = frappe.get_doc({
						"doctype": "Marca Carros",
						"marca": self.make,
						"modelo": self.model
					})
					modelo_camiao.insert()
					frappe.db.commit()
					time.sleep(.300)
					modelo_camiao = frappe.get_list('Marca Carros',fields=['name','modelo'],filters=[['modelo','=',self.model]])
				'''
				except frappe.DoesNotExistError:
					print ('Create Model and Make for Trucks...')
					modelo_camiao = frappe.get_doc({
						"doctype": "Marca Carros",
						"marca": self.make,
						"modelo": self.model
					})
					modelo_camiao.insert()
					frappe.db.commit()
				'''

				print ('Now creates the Truck...')
				print ('modelo_camiao')
				print (modelo_camiao)
				print (type(modelo_camiao))

				print (modelo_camiao[0].name)
				print (modelo_camiao[0].modelo)

				marca_camiao = modelo_camiao[0].name
				modelo_camiao = modelo_camiao[0].modelo

				
				response = frappe.get_doc({
					"doctype": "Veiculos",
					"matricula": self.license_plate,
					"categoria": "Pesados",	#Default for TRucks
					"marca": marca_camiao,
					"modelo": modelo_camiao,
					"veiculo_ano": self.manufacturing_year,
					"veiculo_combustivel": "Gasolina" if self.fuel_type == "Petrol" else "Gasoleo",
					"veiculo_numero_chassi": self.chassis_number,
					"veiculo_codigo_motor": self.engine_number,
					"veiculos_kms": self.odometer_value,
				})
				response.insert()		
				frappe.db.commit()

