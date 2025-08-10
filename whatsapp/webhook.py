import frappe
import requests

@frappe.whitelist(allow_guest=True)
def webhook(doc, method = None):
    try:
        url = "https://n8n.hosting.royalsmb.com/webhook-test/test"
        headers = {
            "Content-Type": "application/json"
        }
        data = doc.as_dict()
        requests.post(url, headers=headers, json=data)
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "WhatsApp Webhook Error")
