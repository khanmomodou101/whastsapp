import frappe

def get_context(context):
    if frappe.session.user == "Guest":
        frappe.redirect("/login")
   
    context.contacts = frappe.db.get_list("Contact", ["*"])
    context.active_page = "contact"
    return context
