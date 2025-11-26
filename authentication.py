# from flask import Flask ,request,jsonify
# from functools import wraps
# import jwt
# from pymongo import MongoClient
# from bson import ObjectId
# import os
# from dotenv import load_dotenv

# load_dotenv()
# app = Flask(__name__)

# app.config['SECRET_KEY']=os.getenv("SECRET_KEY")
# client=MongoClient(os.getenv('MongoClient_URI'))
# db=client["TechbayDB"]
# users=db["user"]

# #logout but token still valid are stored here
# blacklist=set()

# #Authentication Decorator
# def token_required(f):
#     @wraps(f)
#     def decorated(*args,**kargs):
#         auth_header = request.headers.get('Authorization')
#         token = None

#         if auth_header and len(auth_header.split(" ")) == 2:
#             token = auth_header.split(" ")[1]
#         else:
#             return jsonify({'message': 'Token missing in request'}), 400
    
#         if token in blacklist:
#             return jsonify({'message':'Token has been revoked!'}),401

#         try:
#             data=jwt.decode(token,app.config['SECRET_KEY'],algorithms=['HS256'])
#             current_user = users.find_one({'email': data['sub']})

#             if not current_user:
#                 return jsonify({'message':'User not found!'}),401
            
#         except jwt.ExpiredSignatureError:
#             blacklist.add(token)
#             return jsonify({'message':"Token has expired!"}),401
#         except jwt.InvalidTokenError:
#             return jsonify({'message':'Token is invalid!'}),401
        
#         return f(current_user,*args,**kargs)
#     return decorated


# from flask import Flask, request, jsonify
# from functools import wraps
# import jwt
# from pymongo import MongoClient
# from bson import ObjectId
# import os
# from dotenv import load_dotenv
# from datetime import datetime


# load_dotenv()

# app = Flask(__name__)

# # Config
# app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
# client = MongoClient(os.getenv('MongoClient_URI'))
# db = client["TechbayDB"]
# users = db["user"]

# # Token blacklist (for logout/revoked tokens)
# blacklist = set()

# # -------------------------
# # Authentication Decorator
# # -------------------------
# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         auth_header = request.headers.get('Authorization', '')
#         parts = auth_header.split()

#         if len(parts) != 2 or parts[0].lower() != 'bearer':
#             return jsonify({'message': 'Token missing or invalid format'}), 400

#         token = parts[1]

#         # Check if token is blacklisted
#         if token in blacklist:
#             return jsonify({'message': 'Token has been revoked!'}), 401

#         try:
#             # Decode JWT token
#             data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
#             current_user = users.find_one({'email': data['sub']})

#             if not current_user:
#                 return jsonify({'message': 'User not found!'}), 401

#         except jwt.ExpiredSignatureError:
#             # Add expired token to blacklist
#             blacklist.add(token)
#             return jsonify({'message': 'Token has expired!'}), 401
#         except jwt.InvalidTokenError:
#             return jsonify({'message': 'Token is invalid!'}), 401

#         # Pass current_user to the protected route
#         return f(current_user, *args, **kwargs)

#     return decorated
# from flask import Flask ,request,jsonify
# from functools import wraps
# import jwt
# from pymongo import MongoClient
# from bson import ObjectId

# app = Flask(__name__)

# app.config['SECRET_KEY']=os.getenv()
# client=MongoClient('mongodb://localhost:27017/')
# db=client["todo_db"]
# users=db["todouser"]

# #logout but token still valid are stored here
# blacklist=set()

# #Authentication Decorator
# def token_required(f):
#     @wraps(f)
#     def decorated(*args,**kargs):
#         auth_header = request.headers.get('Authorization')
#         token = None

#         if auth_header and len(auth_header.split(" ")) == 2:
#             token = auth_header.split(" ")[1]
#         else:
#             return jsonify({'message': 'Token missing in request'}), 400
    
#         if token in blacklist:
#             return jsonify({'message':'Token has been revoked!'}),401

#         try:
#             data=jwt.decode(token,app.config['SECRET_KEY'],algorithms=['HS256'])
#             current_user=users.find_one({'_id':ObjectId(data['user_id'])})

#             if not current_user:
#                 return jsonify({'message':'User not found!'}),401
            
#         except jwt.ExpiredSignatureError:
#             blacklist.add(token)
#             return jsonify({'message':"Token has expired!"}),401
#         except jwt.InvalidTokenError:
#             return jsonify({'message':'Token is invalid!'}),401
        
#         return f(current_user,*args,**kargs)
#     return decorated

# ####### auth_decorator.py
# from functools import wraps
# from flask import request, jsonify
# import jwt
# import os
# from pymongo import MongoClient

# SECRET_KEY = os.getenv("SECRET_KEY")  # make sure to set this in your .env
# client=MongoClient(os.getenv('MongoClient_URI'))
# db=client["TechbayDB"]
# users=db["users"]
# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         auth_header = request.headers.get('Authorization', '')
#         parts = auth_header.split()

#         if len(parts) != 2 or parts[0].lower() != 'bearer':
#             return jsonify({'message': 'Token missing or invalid format'}), 400

#         token = parts[1]

#         try:
#             payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
#             email = payload.get('sub')  # 'sub' contains the email
#             current_user=users.find_one({"email":email})
#             if not email:
#                 return jsonify({'message': 'Email not found in token'}), 401
            
#             if not current_user:
#                 return jsonify({'message': 'User not found'}), 404
            
#         except jwt.ExpiredSignatureError:
#             return jsonify({'message': 'Token has expired'}), 401
#         except jwt.InvalidTokenError:
#             return jsonify({'message': 'Token is invalid'}), 401

#         return f(current_user, *args, **kwargs)  # pass email to the route

#     return decorated

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
        return f(current_user, **kwargs)

    return decorated
