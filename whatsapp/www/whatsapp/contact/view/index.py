import frappe
def get_context(context):
    if frappe.session.user == "Guest":
        frappe.redirect("/login")
    
    
    context.active_page = "contacts"
    context.id = frappe.request.args.get("id")
    is_editable = True
    
    context.is_editable = is_editable
    return context