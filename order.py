from pymongo import MongoClient
from dotenv import load_dotenv
import os
from flask import Flask,request,jsonify
from bson import ObjectId
from datetime import datetime

load_dotenv()
client = MongoClient(os.getenv('MongoClient_URI'))
db = client["techbay"]
orders = db["orders"]
users=db["users"]
products = db["products"]
addresses=db["addresses"]

# @app.route('/confirmorders', methods=['POST'])
# @token_required
def confirm_order(current_user):
    try:
        user_id = current_user["_id"]
        payment_id = "1234567890"

        # Fetch address
        address = addresses.find_one({"owner": user_id})
        if not address:
            return jsonify({"message": "No address found for this user!"}), 404

        # Fetch cart
        user_data = users.find_one({"_id": user_id}, {"cart": 1})
        
        cart_items = user_data.get("cart", [])
        if not cart_items:
            return jsonify({"message": "Cart is empty!"}), 400

        # --------- NEW: No need to rebuild array -----------
        # Just use the cart directly as products
        order_products = cart_items

        # Calculate total amount
        total_amount = 0
        for item in cart_items:
            product_id = item.get("product_id")
            quantity = item.get("quantity", 1)

            product = products.find_one({"_id": product_id})
            if product:
                total_amount += product.get("price", 0) * quantity
        # ----------------------------------------------------

        # Create order
        new_order = {
            "owner": user_id,
            "address": address["_id"],
            "paymentId": payment_id,
            "products": order_products,        # <--- Direct cart copy
            "amount": total_amount,
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow(),
            "__v": 0
        }

        # Save order
        result = orders.insert_one(new_order)

        # Clear cart
        users.update_one({"_id": user_id}, {"$set": {"cart": []}})

        return jsonify({
            "message": "Order placed successfully!",
            "order_id": str(result.inserted_id),
            "amount": total_amount
        }), 201

    except Exception as e:
        print("Error in confirm_order:", e)
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

# View Orders
# @app.route('/orders', methods=['GET'])
# @token_required
def view_orders(current_user):
    user_id = current_user['_id']
    user_orders = list(orders.find({'owner': ObjectId(user_id)}))
    print(user_orders)
    if not user_orders:
        return jsonify({'message': 'No orders found for this user!'}), 404
    
    # Convert ObjectIds and datetime for JSON response
    for order in user_orders:
        order['_id'] = str(order['_id'])
        order['owner'] = str(order['owner'])
        order['address'] = str(order['address'])
        order['createdAt'] = datetime.utcnow(),
        order["updatedAt"]= datetime.utcnow()
        for p in order['products']:
            p['_id'] = str(p['_id'])
            p['product'] = str(p['product'])
    print(user_orders)
    return jsonify({'orders': user_orders}), 200


# Cancel Order
# @app.route('/cancelorder/<order_id>', methods=['DELETE'])
# @token_required
def cancel_order(current_user, order_id):
    user_id = current_user['_id']

    order = orders.find_one({'_id': ObjectId(order_id), 'owner': user_id})
    if not order:
        return jsonify({'message': 'Order not found!'}), 404

    orders.delete_one({'_id': ObjectId(order_id)})

    return jsonify({'message': 'Order cancelled successfully!'}), 200
