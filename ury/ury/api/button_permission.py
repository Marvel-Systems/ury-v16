import frappe


@frappe.whitelist()
def cancel_check():
    return frappe.has_permission("POS Invoice", "cancel", throw=False)
