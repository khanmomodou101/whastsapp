import frappe

def get_context(context):
    # Get employee ID from URL
    context.active_page = "messages"
    context.title = "New Message"
    context.url = f"whatsapp-message"
    
    return context
    