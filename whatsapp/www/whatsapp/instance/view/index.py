import frappe

def get_context(context):
    # Get employee ID from URL
    id = frappe.form_dict.get('id')
    context.id = id
    context.active_page = "dashboard"
    context.title = frappe.db.get_value("WhatsApp Instance", id, "label")
    context.url = f"instance/{id}"
    context.is_editable = False
    context.refresh_enabled = True  # Enable refresh QR code functionality
    
    return context