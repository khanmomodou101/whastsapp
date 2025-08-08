"""Webhook."""
import frappe
import json
import requests
import time
from werkzeug.wrappers import Response
import frappe.utils
from whatsapp.utils import (
    greet_user, send_catalog, request_location, send_delivery_options,
    ask_for_delivery_options, handle_delivery_selection, handle_location_received,
    send_order_confirmation_with_delivery
)
from whatsapp.whatsapp.doctype.chat_session.chat_session import get_or_create_session


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
		
		# Get or create chat session
		session = get_or_create_session(from_number)
		
		if message_type == "text":
			handle_text_message(from_number, message["text"]["body"], session)
		elif message_type == "interactive":
			handle_interactive_message(from_number, message["interactive"], session)
		elif message_type == "location":
			handle_location_message(from_number, message["location"], session)
		
		return True
	except Exception as e:
		frappe.log_error(f"Error handling message: {str(e)}", "WhatsApp Message Handler")
		return False

def handle_text_message(from_number, text, session):
	"""Handle text messages based on current step."""
	text = text.lower().strip()
	
	# Update session with last message
	session.update_session(last_message=text)
	
	if session.current_step == "Greeting":
		if text in ["hi", "hello", "hey", "hy"]:
			greet_user(from_number)
			session.update_session(
				current_step="Service_Selection",
				last_bot_message="Greeting sent"
			)
		else:
			# Send greeting anyway for any text
			greet_user(from_number)
			session.update_session(
				current_step="Service_Selection",
				last_bot_message="Greeting sent"
			)
	
	elif session.current_step == "Service_Selection":
		if text in ["order", "order now", "place order"]:
			send_catalog(from_number)
			session.update_session(
				current_step="Delivery_Options",
				last_bot_message="Catalog sent"
			)
		else:
			# Send order options
			send_catalog(from_number)
			session.update_session(
				current_step="Delivery_Options",
				last_bot_message="Catalog sent"
			)

def handle_interactive_message(from_number, interactive_data, session):
	"""Handle interactive messages (button clicks, list selections)."""
	
	if interactive_data["type"] == "list_reply":
		callback_data = interactive_data["list_reply"]["id"]
		
		if callback_data == "order_now":
			send_catalog(from_number)
			session.update_session(
				current_step="Delivery_Options",
				last_bot_message="Catalog sent"
			)
	
	elif interactive_data["type"] == "button_reply":
		callback_data = interactive_data["button_reply"]["id"]
		
		if callback_data in ["pickup", "delivery"]:
			if callback_data == "delivery":
				request_location(from_number)
				session.update_session(
					current_step="Location_Request",
					last_bot_message="Location request sent"
				)
			else:  # pickup
				send_order_confirmation_with_delivery(from_number, delivery_fee=0)
				session.update_session(
					current_step="Done",
					last_bot_message="Order confirmation sent (pickup)"
				)
				session.close_session()

def handle_location_message(from_number, location_data, session):
	"""Handle location messages."""
	if session.current_step == "Location_Request":
		latitude = location_data["latitude"]
		longitude = location_data["longitude"]
		
		# Store location in session data
		session.update_session(
			current_step="Order_Confirmation",
			last_bot_message="Location received",
			session_data={
				"latitude": latitude,
				"longitude": longitude,
				"delivery_fee": 100
			}
		)
		
		# Send order confirmation with delivery fee
		send_order_confirmation_with_delivery(from_number, delivery_fee=100)
		session.update_session(
			current_step="Done",
			last_bot_message="Order confirmation sent (delivery)"
		)
		session.close_session()

	



