import frappe
from whatsapp.api import get_instance, get_instance_status


def get_context(context):
    if frappe.session.user == "Guest":
        frappe.redirect("/login?redirect-to=/whatsapp")
    instance = frappe.db.get_value("WhatsApp Instance", {"owner": frappe.session.user}, "name")
    status = get_instance_status(instance)
    if status.get("status") == "Closed" or status.get("status") == "Connecting":
        frappe.redirect("/whatsapp/instance")

    data = get_instance(instance).get("_count")
#    
    context.message = data.get("Message")
    context.contact = data.get("Contact")
    context.chat = data.get("Chat")

    
    context.active_page = "dashboard"
    context.title = "WhatsApp"
    context.url = f"whatsapp"