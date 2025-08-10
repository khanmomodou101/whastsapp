import frappe
def get_context(context):
    if frappe.session.user == "Guest":
        frappe.redirect("/login")
    if not frappe.db.exists("Club", {"owner": frappe.session.user}):
        frappe.redirect("/portal/club/new")
    context.active_page = "technicals"
    context.technical = frappe.request.args.get("id")
    context.technical_name = frappe.db.get_value("Technical Team Member", context.technical, "full_name")
    registration_window = frappe.db.get_single_value("League Settings", "registration_window")
    if not registration_window:
        frappe.redirect("/portal/technicals/view?id=" + context.technical)
    return context