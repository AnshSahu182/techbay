from functools import wraps
from flask import request, jsonify
import jwt
import os
from pymongo import MongoClient

SECRET_KEY = os.getenv("SECRET_KEY")
client = MongoClient(os.getenv("MongoClient_URI"))
db = client["techbay"]
users = db["users"]

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return jsonify({'message': 'Token missing or invalid format'}), 400

        token = parts[1]

        try:
            # 🔹 Decode JWT
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

            # 🔹 Extract email from "sub"
            email = payload.get('sub')
            if not email:
                return jsonify({'message': 'Email not found inside token'}), 401

            # 🔹 Find user in DB
            current_user = users.find_one({"email": email})
            if not current_user:
                return jsonify({'message': 'User not found in database'}), 404

        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401

        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid'}), 401

        # 🔹 Pass user object to route
        return f(current_user, *args, **kwargs)

    return decorated
