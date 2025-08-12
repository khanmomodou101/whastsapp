import frappe

def get_context(context):
    # Get employee ID from URL
    id = frappe.form_dict.get('id')
    context.id = id
    context.active_page = "broadcast"
    context.title = frappe.db.get_value("WhatsApp Broadcast", id, "broadcast_name")
    context.url = f"whatsapp-broadcast/{id}"
    context.is_editable = False
    
    return context
    