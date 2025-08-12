import frappe

def get_context(context):
    # Get employee ID from URL
    context.active_page = "broadcast"
    context.title = "New Broadcast"
    context.url = f"whatsapp-broadcast"
    
    return context
    