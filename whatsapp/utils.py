from pywa import WhatsApp
import frappe

from pywa.types import Button, SectionList, Section, SectionRow, ButtonUrl
import uuid


phone="+2206084445"


wa = WhatsApp(
    phone_id='281222978402210',
    token='EAAlXQfMg4WYBOwXInAXRL6DRosO4cYhW8EupZAkel5bxJPbZAnMipygBWTzZAfx9KRPEZBgdZCIvObMOoeaZBuCo24t1TMNo1fGZCjnuQ53OxE9NshZC4UoZCfb4zFwuYLtYJQOB3k10duBtZCszTWW3NcPiaW8yUL97WizKDSAqUmRJLpLcausksZBBARtIQ2XCk6j'
)
ca = WhatsApp(
    phone_id='281222978402210',
    token='EAAlXQfMg4WYBPPS7vGSYmupl2iKZALccdWc89y3EmntgxdDZB6uSOSWd8dZBNAIqhW5pAp8UKUZBYEyd21s3ZC7zCKg3Ly4ivFZBKyHNtXFTsuQz7UZCey6mK4MWHfDnQaZAwkRpEEnlRxVQrORmB6jlqQ1PTY6FJqUGgTU6xb3OlO3bVB3BZCvMPEXZCx4gxZCCWhbCgZDZD'
)
@frappe.whitelist(allow_guest=True)
def send_message(phone):
    wa.send_message(
        to=phone,
        text='Hi! This message sent from pywa!'
    )

@frappe.whitelist(allow_guest=True)
def request_location(phone):
    wa.request_location(
        to=phone,
        text='Please share your location with us.',
    )





@frappe.whitelist(allow_guest=True)
def greet_user(phone):
    response = wa.send_message(
        to=phone,
        header='👋 Hello! Welcome to Jokoor Food Service.',
        text='Please choose an option:',
        footer='⚡ Powered by Jokoor',
        buttons=SectionList(
        button_title='Select an Option',
        sections=[
            Section(

                title='Order Options',

                rows=[

                    SectionRow(

                        title='Place Order',

                        callback_data='order_now',

                        description='Place an order for delivery or pickup',

                    ),

                    SectionRow(

                        title='Track Order',

                        callback_data='track_order',

                        description='Track your order status',

                    ),

                    SectionRow(

                        title='Cancel Order',

                        callback_data='cancel_order',

                        description='Cancel your order',

                    )

                ],

            )

            

        ]
    )
    )

@frappe.whitelist()
def send_order_option(phone):
    """
    This function sends a message to the user with a list of order options.
    either to order from a restaruant or search for a type a prodcut name
    """


    response = wa.send_message(
        to=phone,
        header='🍽 How would you like to order',
        text='Please choose an option:',
        buttons=SectionList(
        button_title='Select an Option',
        sections=[
            Section(

                title='Order Options',

                rows=[

                    SectionRow(

                        title='From a Restaurant',

                        callback_data='order_from_restaurant',

                        description='Order from a restaurant',

                    ),

                    SectionRow(

                        title='Custom Order',

                        callback_data='custom_order',

                        description='Type the name of the product you want to order',

                    ),

                    

                ]

            )

            

        ]
    )
    )

@frappe.whitelist()
def send_catalog(phone):
    """
    This function sends a message to the user with a list of products.
    """
    try:
        ca.send_catalog(
                to=phone,
                body='Check out our catalog!',
                sender="281222978402210"
            )
        # After sending catalog, ask for delivery options
        ask_for_delivery_options(phone)
        return "Catalog sent successfully"
    except Exception as e:
        # If catalog is empty or not available, send a fallback message
        if "Products not found in FB catalog" in str(e):
            ca.send_message(
                to=phone,
                text='Sorry, our catalog is currently empty. Please contact us directly to place your order.'
            )
            return "Catalog is empty, sent fallback message"
        else:
            # Re-raise other exceptions
            raise e
        
@frappe.whitelist()
def update_commerce_settings():
    """
    This function updates the commerce settings.
    """
    ca.update_commerce_settings(
        is_catalog_visible=True,
        is_cart_enabled=True,
    )
    return "Commerce settings updated"
@frappe.whitelist()
def get_commerce_settings():
    """
    This function gets the commerce settings.
    """
    commerce_settings = ca.get_commerce_settings()
    # Convert CommerceSettings object to dictionary for JSON serialization
    return {
        'catalog_id': commerce_settings.catalog_id,
        'is_catalog_visible': commerce_settings.is_catalog_visible,
        'is_cart_enabled': commerce_settings.is_cart_enabled
    }

@frappe.whitelist()
def send_delivery_options(phone = phone):
    #  "🛍 Would you like:\n"
    #     "1️⃣ Pickup\n"
    #     "2️⃣ Delivery"
    response = wa.send_message(
        to=phone,
        header='🛍 Would you like:',
        text='1️⃣ Pickup\n2️⃣ Delivery',
        buttons=[

        Button(title='Pickup', callback_data=f'pickup'),

        Button(title='Delivery', callback_data=f'delivery')

        ]
    
    )
    
@frappe.whitelist()
def indicate_typing(message_id):
    wa.indicate_typing(message_id)
    

@frappe.whitelist()
def send_order_confirmation(phone = phone):
    item_data = ""
   
    items = [
        {
            "name": "item1",
            "quantity": 1,
            "price": 100
        },
        {
            "name": "item2",
            "quantity": 1,
            "price": 100
        }
    ]
    subtotal = 0
    total_amount = 0
    delivery_fee = 100
    for item in items:
        subtotal += item["price"] * item["quantity"]
        item_data += f"{item['name']} -------------------- {item['quantity']} x {item['price']}\n"
    total_amount = subtotal + delivery_fee
    """
    This function sends a message to the user with a list of items.
    """
    message = f"""Thank you for your order! 🛍️

Here are the details:

{item_data}
--------------------
Subtotal: D{subtotal}
Delivery Fee: D{delivery_fee}
--------------------
Total Amount: D{total_amount}

We'll notify you once your order is on the way 🚚
Thank you for shopping with us"""
    
    response = wa.send_message(
        to=phone,
        text=message,
        buttons=ButtonUrl(
            title='Pay Now',
            url='https://www.jokoor.com'
        )
    )
    return "Sent"

@frappe.whitelist()
def send_order_confirmation_with_delivery(phone, delivery_fee=100):
    """
    Send order confirmation with delivery fee included
    """
    item_data = ""
   
    items = [
        {
            "name": "item1",
            "quantity": 1,
            "price": 100
        },
        {
            "name": "item2",
            "quantity": 1,
            "price": 100
        }
    ]
    subtotal = 0
    total_amount = 0
    
    for item in items:
        subtotal += item["price"] * item["quantity"]
        item_data += f"{item['name']} -------------------- {item['quantity']} x {item['price']}\n"
    
    total_amount = subtotal + delivery_fee
    
    message = f"""Thank you for your order! 🛍️

Here are the details:

{item_data}
--------------------
Subtotal: D{subtotal}
Delivery Fee: D{delivery_fee}
--------------------
Total Amount: D{total_amount}

We'll notify you once your order is on the way 🚚
Thank you for shopping with us"""
    
    response = wa.send_message(
        to=phone,
        text=message,
        buttons=ButtonUrl(
            title='Pay Now',
            url='https://www.jokoor.com'
        )
    )
    return "Sent"

@frappe.whitelist()
def ask_for_delivery_options(phone):
    """
    Ask user how they want to receive their order
    """
    response = wa.send_message(
        to=phone,
        header='🛍 How would you like to receive your order?',
        text='Please choose an option:',
        buttons=[
            Button(title='Pickup', callback_data='pickup'),
            Button(title='Delivery', callback_data='delivery')
        ]
    )
    return "Delivery options sent"

@frappe.whitelist()
def handle_delivery_selection(phone, delivery_type):
    """
    Handle user's delivery selection
    """
    if delivery_type == 'delivery':
        # Request location for delivery
        wa.request_location(
            to=phone,
            text='Please share your location for delivery.',
        )
        return "Location request sent"
    elif delivery_type == 'pickup':
        # Send order confirmation without delivery fee
        return send_order_confirmation_with_delivery(phone, delivery_fee=0)
    else:
        # Send error message
        wa.send_message(
            to=phone,
            text='Invalid selection. Please try again.'
        )
        return "Error message sent"

@frappe.whitelist()
def handle_location_received(phone, latitude, longitude):
    """
    Handle when user shares their location
    """
    # Send order confirmation with delivery fee
    return send_order_confirmation_with_delivery(phone, delivery_fee=100)
