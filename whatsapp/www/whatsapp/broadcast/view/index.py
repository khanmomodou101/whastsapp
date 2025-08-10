import frappe
def get_context(context):
    if frappe.session.user == "Guest":
        frappe.redirect("/login")
    if not frappe.db.exists("Club", {"owner": frappe.session.user}):
        frappe.redirect("/portal/club/new")
    context.active_page = "technicals"
    context.technical = frappe.request.args.get("id")
    is_editable = True
    registration_window = frappe.db.get_single_value("League Settings", "registration_window")
    if not registration_window:
        is_editable = False
    context.is_editable = is_editable
    return context