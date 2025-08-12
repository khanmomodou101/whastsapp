import frappe

def get_context(context):
    instance = frappe.request.args.get("instance")
    if instance:
        frappe.db.set_value("User", frappe.session.user, "instance", instance)
        frappe.db.commit()
    context.active_page = "dashboard"
    context.title = "WhatsApp"
    context.url = f"whatsapp"