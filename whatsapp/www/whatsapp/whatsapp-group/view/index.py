import frappe
def get_context(context):
    if frappe.session.user == "Guest":
        frappe.redirect("/login")
    if not frappe.db.exists("Tournament", frappe.request.args.get("id")):
        frappe.redirect("/portal/tournaments")
    context.tournament = frappe.request.args.get("id")
    tournament_doc = frappe.get_doc("Tournament", context.tournament)
    groups = frappe.db.get_list("Group", {"tournament": tournament_doc.name}, order_by="group_name")
    matches = frappe.db.get_list("Match", {"tournament": tournament_doc.name}, ["*"])
    
    context.groups = groups
    context.tournament = tournament_doc
    context.matches = matches
    return context