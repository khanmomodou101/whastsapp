import frappe
import requests

@frappe.whitelist(allow_guest=True)
def connect_instance(instance):
    """Connect WhatsApp instance by calling external webhook"""
    try:
        url = "https://n8n.hosting.royalsmb.com/webhook-test/connect-instance"
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "instance": instance
        }
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            return "OK"
        else:
            frappe.log_error(f"Webhook returned status {response.status_code}", "WhatsApp Webhook Error")
            return "Error"
            
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "WhatsApp Webhook Error")
        return "Error" 