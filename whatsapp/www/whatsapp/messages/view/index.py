import frappe

def get_context(context):
    # Get employee ID from URL
    id = frappe.form_dict.get('id')
    context.id = id
    context.active_page = "messages"
    context.title = frappe.db.get_value("WhatsApp Message", id, "to")
    context.url = f"whatsapp-message/{id}"
    context.is_editable = False
    
    return context
    