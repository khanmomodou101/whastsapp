import frappe

def get_context(context):

    context.active_page = 'contact'
    context.title = "Contact"
    context.add_new_url = "/whatsapp/contact/new"

    if frappe.request.args.get("per_page"):
        per_page = int(frappe.request.args.get("per_page"))
    else:
        per_page = 20
    
    # Define table columns
    context.columns = [
        {"key": "full_name", "label": "Full Name"},
        {"key": "custom_primary_contact", "label": "Phone Number"},
        {"key": "creation", "label": "Created At"},
    ]
    
    # Get employee data
    data = frappe.get_list(
        "Contact", ["name","full_name", "custom_primary_contact", "creation"],
        limit=per_page
    )
    
    # Process employee data
    for d in data:

        doc = frappe.get_doc("Contact", d.name)
        creation = frappe.utils.format_date(doc.creation, "dd-MMM-yyyy")
        d.creation = creation
        d.name = doc.name
        

        d.url = f"/whatsapp/whatsapp-contact/view?id={doc.name}"
        
    context.per_page = per_page 
    context.data = data
