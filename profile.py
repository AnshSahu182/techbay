from pymongo import MongoClient
from dotenv import load_dotenv
import os
from flask import request,jsonify
from bson import ObjectId
from datetime import datetime
import cloudinary
import cloudinary.uploader
load_dotenv()

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
    user = users.find_one(
            {"_id": current_user["_id"]},)
    
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
# @app.route('/updateaddress', methods=['PUT'])
# @token_required
def update_address(current_user):
    data = request.get_json()

    # Find the address for this user
    address = addresses.find_one({"owner": current_user["_id"]})
    if not address:
        return jsonify({"error": "Address not found"}), 404

    # Update allowed fields
    update_data = {
        "address": data.get("address", address.get("address")),
        "mobile": data.get("mobile", address.get("mobile")),
        "city": data.get("city", address.get("city")),
        "state": data.get("state", address.get("state")),
        "pincode": data.get("pincode", address.get("pincode")),
        "type": data.get("type", address.get("type")),
        "updatedAt": datetime.utcnow()
    }

    addresses.update_one(
        {"owner": current_user["_id"]},
        {"$set": update_data}
    )

    return jsonify({"message": "Address updated successfully"}), 200

# Delete Address
# @app.route('/deleteaddress', methods=['DELETE'])
# @token_required
def delete_address(current_user):
    # Find the address for this user
    address = addresses.find_one({"owner": current_user["_id"]})
    if not address:
        return jsonify({"error": "Address not found"}), 404

    # Delete it
    addresses.delete_one({"owner": current_user["_id"]})
    return jsonify({"message": "Address deleted successfully"}), 200

#Logout 
# @app.route("/logout",methods=["POST"])
# @token_required
# def logout(current_user):
    
#     auth_header = request.headers.get('Authorization')
#     if auth_header and len(auth_header.split(" ")) == 2:
#         token = auth_header.split(" ")[1]
#     else:
#         return jsonify({'message': 'Token missing in request'}), 400

   # blacklist.add(token)
    return jsonify({'message':'Logout successful'}),200
