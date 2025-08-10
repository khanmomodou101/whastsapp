import frappe

def get_context(context):
    context.active_page = 'dashboard'
    return context 