import frappe

from frappe.utils.jinja_globals import bundled_asset, include_script, include_style

def get_context(context):
    context.khan = bundled_asset('bootstrap.bundle.min.js')