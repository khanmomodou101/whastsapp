# Copyright (c) 2025, royalsmb and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime

class ChatSession(Document):
    def before_save(self):
        """Update last_updated timestamp before saving."""
        self.last_updated = now_datetime()
    
    def update_session(self, current_step=None, last_message=None, last_bot_message=None, session_data=None):
        """Update session with new data."""
        if current_step:
            self.current_step = current_step
        if last_message:
            self.last_message = last_message
        if last_bot_message:
            self.last_bot_message = last_bot_message
        if session_data:
            if not self.session_data:
                self.session_data = {}
            self.session_data.update(session_data)
        
        self.save()
    
    def close_session(self):
        """Close the chat session."""
        self.status = "Closed"
        self.current_step = "Done"
        self.save()

@frappe.whitelist()
def get_or_create_session(wa_id, profile_name=None):
    """Get existing session or create new one."""
    existing_session = frappe.db.exists("Chat Session", {"wa_id": wa_id, "status": "Active"})
    
    if existing_session:
        return frappe.get_doc("Chat Session", existing_session)
    else:
        # Create new session
        session = frappe.get_doc({
            "doctype": "Chat Session",
            "wa_id": wa_id,
            "profile_name": profile_name,
            "current_step": "Greeting",
            "status": "Active",
            "session_data": {}
        })
        session.insert(ignore_permissions=True)
        frappe.db.commit()
        return session 