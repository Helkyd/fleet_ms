# Copyright (c) 2023, VV SYSTEMS DEVELOPER LTD and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import time

#Last Modified: 01-09-2026

class Trailers(Document):
	def before_save(self):
		if not self.trailer_number:
			self.trailer_number = self.plate_number


	def on_update(self):
		#FIX 01-09-2026; Check if Officinas app installed
		print ('on update TRAILER... ', self.plate_number)
		print ('Apps installed ', frappe.get_installed_apps())
		print ("aoerp_oficinas" in frappe.get_installed_apps())
		if "aoerp_oficinas" in frappe.get_installed_apps():
			#FIX 04-08-2026; Added ignore_permissions
			camiao = frappe.get_list('Veiculos',fields=['name'],filters=[['name','=',self.plate_number]],ignore_permissions=True)
			if camiao == []:
				print ('Truck does not existe.... creating...')
				modelo_camiao = frappe.get_list('Marca Carros',fields=['name','modelo'],filters=[['modelo','=',self.trailer_make]],ignore_permissions=True)
				if modelo_camiao == []:
					print ('Create Model and Make for Trucks...')
					modelo_camiao = frappe.get_doc({
						"doctype": "Marca Carros",
						"marca": self.trailer_make,
						"modelo": self.trailer_make
					})
					modelo_camiao.insert(ignore_permissions=True)
					frappe.db.commit()
					time.sleep(.300)
					modelo_camiao = frappe.get_list('Marca Carros',fields=['name','modelo'],filters=[['modelo','=',self.trailer_make]],ignore_permissions=True)

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
					"matricula": self.plate_number,
					"categoria": "Pesados",	#Default for TRucks
					"marca": marca_camiao,
					"modelo": modelo_camiao,
					"veiculo_ano": self.manufacturing_year,
					"veiculo_combustivel": "Gasoleo",	#Default
					"veiculo_numero_chassi": self.chassis_number,
					#"veiculo_codigo_motor": self.engine_number,
					#"veiculos_kms": self.odometer_value,
					"pertence_empresa": 1,	#Default
				})
				response.insert(ignore_permissions=True)
				frappe.db.commit()

