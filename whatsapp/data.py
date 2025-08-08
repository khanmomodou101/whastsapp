"""Webhook."""
import frappe
import json
import requests
import time
from werkzeug.wrappers import Response
import frappe.utils
from whatsapp.utils import greet_user, send_catalog, request_location, send_delivery_options


@frappe.whitelist(allow_guest=True)
def webhook():
	"""Meta webhook."""
	if frappe.request.method == "GET":
		return get()
	return post()


def get():
	"""Get."""
	hub_challenge = frappe.form_dict.get("hub.challenge")
	webhook_verify_token = "royalsmb"

	if frappe.form_dict.get("hub.verify_token") != webhook_verify_token:
		frappe.throw("Verify token does not match")

	return Response(hub_challenge, status=200)

def post():
	try:
		"""Post."""
		data = frappe.request.json

		# Check if message has already been processed
		message = data["entry"][0]["changes"][0]["value"]["messages"][0]
		message_id = message.get("id")
		
		if message_id:
			# Check if this message ID already exists in the database
			existing = frappe.db.exists("WhatsApp Data", {"data": ["like", f"%{message_id}%"]})
			if existing:
				return Response(status=200)

		handle_message(data)
		
		# Save the processed message data
		doc = frappe.get_doc("WhatsApp Data")
		doc.data = json.dumps(data)
		doc.insert(ignore_permissions=True)
		frappe.db.commit()
		
		return Response(status=200)
	except Exception as e:
		frappe.db.rollback()
		frappe.log_error(frappe.get_traceback(), "WhatsApp Webhook Error")
		return Response(status=500)


@frappe.whitelist(allow_guest=True)
def handle_message(data):
	"""Handle incoming WhatsApp messages."""
	try:
		message = data["entry"][0]["changes"][0]["value"]["messages"][0]
		message_type = message["type"]
		from_number = message["from"]

		if message_type == "text":
			greet_user(from_number)
		elif message_type == "interactive":
			if (message["interactive"]["type"] == "list_reply" and 
				message["interactive"]["list_reply"]["id"] == "order_now"):
				send_catalog(from_number)
		
		return True
	except Exception as e:
		frappe.log_error(f"Error handling message: {str(e)}", "WhatsApp Message Handler")
		return False

	



