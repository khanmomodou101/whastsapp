import frappe

def get_context(context):

    context.active_page = 'dashboard'
    context.title = "Instance"
    context.add_new_url = "/whatsapp/instance/new"

    if frappe.request.args.get("per_page"):
        per_page = int(frappe.request.args.get("per_page"))
    else:
        per_page = 20
    
    # Define table columns
    context.columns = [
        {"key": "label", "label": "Label"},
        {"key": "phone_number", "label": "Phone Number"},
        {"key": "created_at", "label": "Created At"},
    ]
    
    # Get employee data
    data = frappe.get_list(
        "WhatsApp Instance", ["name","label","phone_number", 'creation'],
        limit=per_page
    )
    
    # Process employee data
    for d in data:

        doc = frappe.get_doc("WhatsApp Instance", d.name)
        creation = frappe.utils.format_date(doc.creation, "dd-MMM-yyyy")
        d.creation = creation
        d.name = doc.name
        

        d.url = f"/whatsapp/instance/view?id={doc.name}"
        
    context.per_page = per_page 
    context.data = data
