from pymongo import MongoClient
from dotenv import load_dotenv
import os
from flask import request,jsonify
from bson import ObjectId
from datetime import datetime
import cloudinary
import cloudinary.uploader
from flask_bcrypt import Bcrypt

load_dotenv()
bcrypt= Bcrypt()
cloudinary.config(
    secure = True,
    api_key = os.getenv("CLOUDINARY_API_KEY"),
    api_secret = os.getenv("CLOUDINARY_SECRET_KEY"))

client=MongoClient(os.getenv('MongoClient_URI'))
db=client["techbay"]
users=db["users"]
addresses=db["addresses"]

#View User Details
# @app.route("/profile", methods=['GET'])
# @token_required
def user_details(current_user):
    user = users.find_one(
        {"_id": current_user["_id"]},
        {"username": 1, "email": 1, "image": 1})
    if user:
        user["_id"] = str(user["_id"])
        return jsonify(user), 200
    else:
        return jsonify({"message": "User not found"}), 404

# @app.route('/upload-profile-photo', methods=['POST'])
def upload_profile_photo(current_user):
    try:
        file = request.files.get('image')

        if not file:
            return jsonify({"error": "Image file required"}), 400

        # Upload to Cloudinary
        result = cloudinary.uploader.upload(
            file,
            folder="users/profile"
        )

        image_url = result.get("secure_url")

        # Save only URL
        users.update_one(
            {"_id": current_user["_id"]},
            {
                "$set": {
                    "image": image_url,
                    "updatedAt": datetime.utcnow()
                }
            }
        )

        return jsonify({
            "message": "Profile photo updated",
            "image_url": image_url
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Add Address
# @app.route("/addaddress", methods=['POST'])
# @token_required
def add_address(current_user):
    data = request.get_json()
    user = users.find_one(
            {"_id": current_user["_id"]})

    # Extract all the fields from request
    owner = str(user["_id"])
    name = data.get('name')
    address = data.get('address')
    mobile = data.get('mobile')
    city = data.get('city')
    state = data.get('state')
    pincode = data.get('pincode')
    type_ = data.get('type')  # 'type' is a reserved word, so use type_

    # Basic validation
    if not all([owner, name, address, mobile, city, state, pincode, type_]):
        return jsonify({"error": "All required fields must be filled"}), 400

    # Prepare document
    new_address = {
        "owner": ObjectId(owner),  # convert string id to ObjectId
        "name": name,
        "address": address,
        "mobile": mobile,
        "city": city,
        "state": state,
        "pincode": pincode,
        "type": type_,
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    }

    # Insert into new collection 'address'
    addresses.insert_one(new_address)

    return jsonify({"message": "Address added successfully"}), 201

# View address
# @app.route('/viewaddress', methods=['GET'])
# @token_required
def view_address(current_user):
    
    address_cursor = addresses.find(
        {"owner": current_user["_id"]},
        {"_id": 1,"name":1,"mobile":1, "address": 1, "city": 1, "state": 1, "pincode": 1, "type": 1})

    address_list = list(address_cursor)

    if not address_list:
        return jsonify({"error": "No addresses found"}), 404

    # Convert ObjectId to string for JSON serialization
    for addr in address_list:
        addr["_id"] = str(addr["_id"])

    return jsonify({"address": address_list}), 200

#Update Address
def update_address(current_user, address_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data received"}), 400

    # Get address and ownership check
    address = addresses.find_one({
        "_id": ObjectId(address_id),
        "owner": current_user["_id"]
    })

    if not address:
        return jsonify({"error": "Address not found"}), 404

    update_data = {}
    allowed_fields = ["address","name", "mobile", "city", "state", "pincode", "type"]

    # ONLY update fields sent from frontend
    for field in allowed_fields:
        if field in data:
            update_data[field] = data[field]

    if not update_data:
        return jsonify({"message": "No changes provided"}), 200

    update_data["updatedAt"] = datetime.utcnow()

    result = addresses.update_one(
        {"_id": ObjectId(address_id)},
        {"$set": update_data}
    )

    if result.modified_count == 0:
        return jsonify({"message": "No changes made"}), 200

    return jsonify({"message": "Address updated successfully"}), 200

# Delete Address
# @app.route('/deleteaddress', methods=['DELETE'])
# @token_required
def delete_address(current_user,address_id):
    # Find the address for this user
    address = addresses.find_one({"_id":ObjectId(address_id)})
    if not address:
        return jsonify({"error": "Address not found"}), 404

    # Delete it
    addresses.delete_one({"_id": ObjectId(address_id)})
    return jsonify({"message": "Address deleted successfully"}), 200

# Change password
# @app.route('/change_password',methods=['POST'])
def change_user_password(current_user):
    try:
        data = request.get_json()
        old_password = data.get("currentPassword")
        new_password = data.get("newPassword")

        if not old_password or not new_password:
            return jsonify({"message": "Both fields are required"}), 400

        # new password must be different
        if old_password == new_password:
            return jsonify({"message": "New password must be different"}), 400

        # find user in MongoDB
        user = users.find_one({"_id": current_user["_id"]})
        if not user:
            return jsonify({"message": "User not found"}), 404

        # check old password
        if not bcrypt.check_password_hash(user["password"], old_password):
            return jsonify({"message": "Invalid old password"}), 401

        # hash new password
        hashed_new_pw = bcrypt.generate_password_hash(new_password).decode("utf-8")

        # update password in DB
        users.update_one(
            {"_id": user["_id"]},
            {"$set": {
                "password": hashed_new_pw,
                "updatedAt": datetime.utcnow()
            }}
        )

        return jsonify({"message": "Password changed successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500