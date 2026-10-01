from __future__ import unicode_literals
import frappe
from frappe import _


def set_dimension(src_doc, tr_doc, src_child=None, tr_child=None):
	set = frappe.get_cached_doc("Transport Settings", "Transport Settings")
	if len(set.accounting_dimension) == 0:
		return
	for dim in set.accounting_dimension:
		if (
			dim.source_doctype == src_doc.doctype
			and dim.target_doctype == tr_doc.doctype
		):
			value = None

			if dim.source_type == "Field":
				value = src_doc.get(dim.source_field_name)
			elif dim.source_type == "Value":
				value = dim.value
			elif dim.source_type == "Child" and src_child:
				value = src_child.get(dim.child_field_name)
			
			if dim.target_type == "Main":
				setattr(tr_doc, dim.target_field_name, value)
			elif dim.target_type == "Child" and tr_child:
				setattr(tr_child, dim.target_child_field_name, value)


#FIX 01-10-2026; Update existing Sales Order with Truck Dimensions
@frappe.whitelist()
def update_existing_so_dimension():
	#Last Modified: 01-10-2026
	for existing_so in frappe.get_all('Sales Order',filters={'docstatus':1},fields={'name'}):
		doc = frappe.get_doc('Sales Order', existing_so.name)
		for it in doc.items:
			if it.prevdoc_docname:
				#For sure is a Quotation...
				proforma = frappe.get_doc('Quotation', it.prevdoc_docname)
				for pfitem in proforma.items:
					if pfitem.cargo_id:
						manifesto = frappe.get_all('Manifest Cargo Details', filters={'cargo_id':pfitem.cargo_id},fields={'parent','specific_cargo_allocated'})
						if manifesto != []:
							print ('Allocated TRuck Dimension on Sales Order....')
							#it.truck = manifesto[0]['specific_cargo_allocated']
							frappe.db.sql(""" UPDATE `tabSales Order Item` set truck = %s where parent = %s """,(manifesto[0]['specific_cargo_allocated'],existing_so.name), as_dict=False)
							#Sets only one Truck on the main SO
							if doc.truck == [] or doc.truck == None:
								doc.truck = manifesto[0]['specific_cargo_allocated']
								frappe.db.sql(""" UPDATE `tabSales Order` set truck = %s where name = %s """,(manifesto[0]['specific_cargo_allocated'],existing_so.name), as_dict=False)
						
							frappe.db.commit()

							#Now to on Sales Invoices if exists...
							print ('Allocated TRuck Dimension on Sales Invoices....')
							#it.truck = manifesto[0]['specific_cargo_allocated']
							frappe.db.sql(""" UPDATE `tabSales Invoice Item` set truck = %s where parent = %s """,(manifesto[0]['specific_cargo_allocated'],existing_so.name), as_dict=False)
						
							frappe.db.commit()


		


