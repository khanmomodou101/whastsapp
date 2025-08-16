import frappe

def get_context(context):
    # Get employee ID from URL
    id = frappe.form_dict.get('id')
    context.id = id
    context.active_page = "contact"
    context.title = frappe.db.get_value("WhatsApp Contact", id, "full_name")
    context.url = f"whatsapp-contact/{id}"
    context.is_editable = False
    
    return context
    