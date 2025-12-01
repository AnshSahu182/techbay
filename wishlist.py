from pymongo import MongoClient
from dotenv import load_dotenv
import os
from flask import jsonify
from bson import ObjectId

load_dotenv()

client=MongoClient(os.getenv('MongoClient_URI'))
db=client["techbay"]
users=db["users"]
products=db["products"]

# Add to Wishlist
def add_to_wishlist(current_user, product_id):
    try:
        
        if not product_id:
            return jsonify({"error": "Product ID is required"}), 400

        user = users.find_one({"_id": current_user["_id"]})
        if not user:
            return jsonify({"error": "User not found"}), 404

        wishlist = user.get("wishlist", [])

        # Check if product already exists in wishlist
        for item in wishlist:
            if str(item["product_id"]) == product_id:
                return jsonify({"message": "Product already in wishlist"}), 200

        # Add the new product
        wishlist.append({
            "_id": ObjectId(),
            "product_id": ObjectId(product_id)
        })

        # Save changes
        users.update_one(
            {"_id": current_user["_id"]},
            {"$set": {"wishlist": wishlist}}
        )

        return jsonify({"message": "Product added to wishlist successfully"}), 200

    except Exception as e:
        print("Error in add_to_wishlist:", e)
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


# View Wishlist
def view_wishlist(current_user):
    user = users.find_one({"_id": current_user["_id"]})
    
    wishlist = user.get('wishlist', [])
    products_list = []

    for item in wishlist:
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
                "product_details": product
            })


    return jsonify({
        "message": "Wishlist fetched successfully",
        "wishlist": products_list
    }), 200

# Delete from Wishlist
def delete_from_wishlist(current_user,product_id):

    if not product_id:
        return jsonify({"error": "Product ID is required"}), 400

    user = users.find_one({"_id": current_user["_id"]})
    if not user:
        return jsonify({"error": "User not found"}), 404

    wishlist = user.get("wishlist", [])

    # Filter out the product to remove it
    updated_wishlist = [
        item for item in wishlist if str(item.get("product_id")) != str(product_id)
    ]

    # Update user wishlist in DB
    users.update_one(
        {"_id": current_user["_id"]},
        {"$set": {"wishlist": updated_wishlist}}
    )

    return jsonify({"message": "Product removed from wishlist successfully"}), 200
