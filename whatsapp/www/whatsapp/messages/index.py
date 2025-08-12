import frappe

def get_context(context):

    context.active_page = 'messages'
    context.title = "Messages"
    context.add_new_url = "/whatsapp/messages/new"

    if frappe.request.args.get("per_page"):
        per_page = int(frappe.request.args.get("per_page"))
    else:
        per_page = 20
    
    # Define table columns
    context.columns = [
        {"key": "to", "label": "To"},
        {"key": "content_type", "label": "Type"},
        {"key": "status", "label": "Status"},
        {"key": "created_at", "label": "Created At"},
    ]
    
    # Get employee data
    data = frappe.get_list(
        "WhatsApp Message", ["name","to", "content_type", "status", 'creation'],
        limit=per_page
    )
    
    # Process employee data
    for d in data:

        doc = frappe.get_doc("WhatsApp Message", d.name)
        creation = frappe.utils.format_date(doc.creation, "dd-MMM-yyyy")
        d.creation = creation
        d.name = doc.name
        

        d.url = f"/whatsapp/messages/view?id={doc.name}"
        
    context.per_page = per_page 
    context.data = data
