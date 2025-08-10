import frappe
def get_context(context):
    if frappe.session.user == "Guest":
        frappe.redirect("/login")
    if not frappe.db.exists("Club", {"owner": frappe.session.user}):
        frappe.redirect("/portal/club/new")
    context.active_page = "technicals"
    club = frappe.get_doc("Club", {"owner": frappe.session.user})
    registration_window = frappe.db.get_single_value("League Settings", "registration_window")
    if not registration_window:
        frappe.redirect("/portal/technicals")
    count = frappe.db.count("Technical Team Member", {"club": club.name})
    if count >= 5:
        frappe.redirect("/portal/technicals")
    return context