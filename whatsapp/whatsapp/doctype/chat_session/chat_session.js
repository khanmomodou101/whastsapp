// Copyright (c) 2025, royalsmb and contributors
// For license information, please see license.txt

frappe.listview_settings['Chat Session'] = {
	add_fields: ["status", "current_step", "last_updated"],
	get_indicator: function(doc) {
		if (doc.status === "Active") {
			return [__("Active"), "green", "status,=,Active"];
		} else if (doc.status === "Closed") {
			return [__("Closed"), "red", "status,=,Closed"];
		}
	},
	order_by: "last_updated desc"
}; 