import frappe

def get_context(context):
    if frappe.session.user == "Guest":
        frappe.redirect("/login")
    if not frappe.db.exists("Club", {"owner": frappe.session.user}):
        frappe.redirect("/portal/club/new")
    context.active_page = "players"
    club = frappe.get_doc("Club", {"owner": frappe.session.user})
    if frappe.session.user == "Administrator":
        club = frappe.get_doc("Club", "FC Revolution")
    context.club = club
    context.players = frappe.db.get_list("Player", {"club": club.name}, ["*"])
    registration_window = frappe.db.get_single_value("League Settings", "registration_window")
    can_add = True
    if not registration_window:
        can_add = False
    context.can_add = can_add
    count = frappe.db.count("Player", {"club": club.name})
    if count >= 25:
        can_add = False
    context.can_add = can_add
    return context
