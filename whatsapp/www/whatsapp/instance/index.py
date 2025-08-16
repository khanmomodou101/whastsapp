import frappe
from whatsapp.api import get_instance_status, connect_instance



def get_context(context):
    # Get employee ID from URL
    id = frappe.get_doc("WhatsApp Instance", {"owner": frappe.session.user}).name
    status = get_instance_status(id)
    if status.get("status") == "Open":
        frappe.redirect("/whatsapp")
    else:
        connect_instance(id)

    context.id = id
    context.active_page = "dashboard"
    context.title = frappe.db.get_value("WhatsApp Instance", id, "label")
    context.url = f"instance/{id}"
    context.subtitle = frappe.db.get_value("WhatsApp Instance", id, "status")
    
    return context