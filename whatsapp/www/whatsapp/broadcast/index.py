import frappe

def get_context(context):
    if frappe.session.user == "Guest":
        frappe.redirect("/login")
    if not frappe.db.exists("Club", {"owner": frappe.session.user}):
        frappe.redirect("/portal/club/new")
    context.active_page = "technicals"
    club = frappe.get_doc("Club", {"owner": frappe.session.user})
    if frappe.session.user == "Administrator":
        club = frappe.get_doc("Club", "FC Revolution")
    context.club = club
    context.technicals = frappe.db.get_list("Technical Team Member", {"club": club.name}, ["*"])
    can_add = True
    registration_window = frappe.db.get_single_value("League Settings", "registration_window")
    if not registration_window:
        can_add = False
    count = frappe.db.count("Technical Team Member", {"club": club.name})
    if count >= 5:
        can_add = False
    context.can_add = can_add
    return context
