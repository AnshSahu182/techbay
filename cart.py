from pymongo import MongoClient
from dotenv import load_dotenv
import os
from flask import request,jsonify
from bson import ObjectId

load_dotenv()

client=MongoClient(os.getenv('MongoClient_URI'))
db=client["techbay"]
users=db["users"]
products=db["products"]

# Add to cart
def add_to_cart(current_user):
    data = request.get_json()
    product_id = data.get("product_id")
    quantity = int(data.get("quantity", 1))

    if not product_id:
        return jsonify({"error": "Product ID not found"}), 400

    product_id = ObjectId(product_id)

    user = users.find_one({"email": current_user["email"]})
    if not user:
        return jsonify({"error": "User not found"}), 404

    cart = current_user.get("cart", [])
    found = False

    # Loop through existing cart items
    for item in cart:
        # check if this product already exists in cart
        if item.get("product_id") == product_id:
            item["quantity"] += quantity
            found = True
            break

    # if not found, add new entry
    if not found:
        cart.append({
            "product_id": product_id,
            "quantity": quantity
        })

    # update user document
    users.update_one(
        {"_id": current_user["_id"]},
        {"$set": {"cart": cart}}
    )

    return jsonify({"message": "Product added to cart successfully"}), 200


# View cart
def view_cart(current_user):
    user = users.find_one({"_id": current_user["_id"]})
    
    cart = user.get('cart', [])
    products_list = []

    for item in cart:
    # Convert ObjectId to string for JSON safety
        product_id = item.get("product_id")
        if isinstance(product_id, ObjectId):
            product_id = str(product_id)
            
    # Fetch product details
        product = products.find_one(
            {"_id": ObjectId(item['product_id'])},
            {"title": 1,"image":1, "description": 1, "price": 1, "_id": 0}
        )

        if product:
            products_list.append({
                "product_id": product_id,
                "quantity": item.get("quantity", 1),
                "product_details": product
            })

    return jsonify({
    "message": "Cart fetched successfully",
    "cart": products_list
    }), 200


# Delete product from cart
def delete_from_cart(current_user):
    data = request.get_json()
    product_id = data.get("product_id")

    if not product_id:
        return jsonify({"error": "Product ID is required"}), 400

    user = users.find_one({"email": current_user["email"]})
    if not user:
        return jsonify({"error": "User not found"}), 404

    cart = user.get("cart", [])

    # Remove the product from cart if it exists
    new_cart = [item for item in cart if str(item.get("product_id")) != product_id]

    if len(new_cart) == len(cart):
        return jsonify({"error": "Product not found in cart"}), 404

    users.update_one(
        {"_id": current_user["_id"]},
        {"$set": {"cart": new_cart}}
    )

    return jsonify({"message": "Product removed from cart successfully"}), 200

# Reduce quantity
def reduce_from_cart(current_user):
    data = request.get_json()
    product_id = data.get("product_id")
    quantity = int(data.get("quantity", 1))

    if not product_id:
        return jsonify({"error": "Product ID not found"}), 400

    user = users.find_one({"_id": current_user["_id"]})
    if not user:
        return jsonify({"error": "User not found"}), 404

    cart = user.get("cart", [])
    updated_cart = []

    product_found = False
    for item in cart:
        # Convert stored product ObjectId to str for comparison
        if str(item.get("product_id")) == str(product_id):
            product_found = True
            new_quantity = item.get("quantity", 0) - quantity
            if new_quantity > 0:
                item["quantity"] = new_quantity
                updated_cart.append(item)
            # if new_quantity <= 0, we skip adding -> remove from cart
        else:
            updated_cart.append(item)

    if not product_found:
        return jsonify({"error": "Product not found in cart"}), 404

    users.update_one(
        {"_id": current_user["_id"]},
        {"$set": {"cart": updated_cart}}
    )

    return jsonify({"message": "Product quantity reduced successfully"}), 200