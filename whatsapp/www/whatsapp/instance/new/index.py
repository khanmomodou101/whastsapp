import frappe

def get_context(context):
    # Get employee ID from URL
    context.active_page = "dashboard"
    context.title = "New Instance"
    context.url = f"instance/new"
    
    return context
    