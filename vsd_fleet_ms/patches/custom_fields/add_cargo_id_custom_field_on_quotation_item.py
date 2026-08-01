import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def execute():
    fields = {
        "Quotation Item": [
            {
                "fieldname": "cargo_id",
                "fieldtype": "Data",
                "label": "Cargo ID",
                "insert_after": "stock_balance",
                "read_only": 1
            }
        ]
    }
    create_custom_fields(fields, update=True)
    frappe.reload_doc("selling", "doctype", "quotation_item", force=True)
