import frappe

def get_context(context):
    context.active_page = "tournaments"
    if frappe.session.user == "Guest":
        frappe.redirect("/login")
    if not frappe.db.exists("Club", {"owner": frappe.session.user}):
        frappe.redirect("/portal/club/new")
    club = frappe.get_doc("Club", {"owner": frappe.session.user})
    club.flags.ignore_permissions = True
    
    
    context.club = club
    team_tables = frappe.db.get_list("Teams Table", {"club": club.name, "parenttype": "Tournament"}, ["*"])
    tournament_tables = []
    for team_table in team_tables:
        doc = frappe.db.get_value("Teams Table", {"name": team_table.name}, "parent")
        tournament_tables.append({
            "name": doc
        })
   
    context.tournaments = tournament_tables
    return context
