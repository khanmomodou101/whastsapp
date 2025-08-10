import frappe
def get_context(context):
    if frappe.session.user == "Guest":
        frappe.redirect("/login")
   
    context.active_page = "contacts"
    context.id = frappe.request.args.get("id")
    context.name = frappe.db.get_value("Contact", context.id, "full_name")
    
    return context