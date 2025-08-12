import frappe

def get_context(context):

    context.active_page = 'broadcast'
    context.title = "Broadcast"
    context.add_new_url = "/whatsapp/broadcast/new"

    if frappe.request.args.get("per_page"):
        per_page = int(frappe.request.args.get("per_page"))
    else:
        per_page = 20
    
    # Define table columns
    context.columns = [
        {"key": "broadcast_name", "label": "Broadcast Name"},
        {"key": "instance", "label": "Instance"},
        {"key": "group", "label": "Group"},
        {"key": "created_at", "label": "Created At"},
    ]
    
    # Get employee data
    data = frappe.get_list(
        "WhatsApp Broadcast", ["broadcast_name","instance", "group", 'creation'],
        limit=per_page
    )
    
    # Process employee data
    for d in data:

        doc = frappe.get_doc("WhatsApp Broadcast", d.name)
        creation = frappe.utils.format_date(doc.creation, "dd-MMM-yyyy")
        d.creation = creation
        d.name = doc.name
        

        d.url = f"/whatsapp/broadcast/view?id={doc.name}"
        
    context.per_page = per_page 
    context.data = data
