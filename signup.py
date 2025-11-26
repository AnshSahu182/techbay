from flask import Flask,request,jsonify, url_for,session
from authlib.integrations.flask_client import OAuth # for login
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, create_refresh_token,JWTManager
from flask_cors import CORS
from datetime import datetime

load_dotenv()

# app=Flask(__name__)
bcrypt=Bcrypt()
# CORS(app)
# app.secret_key=os.getenv('SECRET_KEY')
# app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
# jwt = JWTManager(app)


client=MongoClient(os.getenv('MongoClient_URI'))
db=client["techbay"]
users=db["users"]

# 🔑 Google OAuth Configuration
oauth = OAuth()
google = oauth.register(
    name='google',
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('CLIENT_SECRET'),
    access_token_url='https://oauth2.googleapis.com/token',
    authorize_url='https://accounts.google.com/o/oauth2/v2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v2/',
    client_kwargs={'scope': 'openid email profile'},
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration'
)


# Sign up using google
# @app.route('/googlesignup', methods=['GET'])
def google_signup():
    redirect_uri=url_for('callback',_external=True)
    return google.authorize_redirect(redirect_uri)

#Login using google
# @app.route('/googlelogin', methods=['POST'])
#data here does not goto server it goes to google and it send redirected url that is why there is GET 
def google_login():
    redirect_uri=url_for('callback',_external=True)
    return google.authorize_redirect(redirect_uri)

#Callback (Direct google login ka data deta h )
#@app.route("/callback", methods=['GET'])
#data here does not go to server it goes to google and it send redirected url that is why there is GET 
def callback():
    token=google.authorize_access_token()  # exchange code for token
    user_info=google.get('userinfo').json() #get user data from token

    email=user_info.get('email')
    name=user_info.get('name')
    picture=user_info.get("picture")

    user=users.find_one({'email':email})
    if  user:
        users.update_one(
            {'email':email},{"$set":{"image":picture,"updatedAt":datetime.utcnow()}})
        
    else:
        users.insert_one({
            "username":name,
            "email":email,
            "password":None,
            "image":picture,
            "createdAt":datetime.utcnow(),
            "updatedAt":datetime.utcnow(),
            "refreshToken":None
        })
    access_token=create_access_token(identity=email)
    refresh_token=create_refresh_token(identity=email)
    users.update_one(
        {"email":email},
        {"$set":{"refreshToken":refresh_token}}
    )

    return jsonify({
        "message":"Login successful",
        "email":email,
        "access_token":access_token,
        "refresh_token":refresh_token
    })


## Normal Signup
#@app.route('/signup', methods=['POST'])
def normal_signup():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid or missing JSON data"}), 400

        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        confirmPassword = data.get('confirmPassword')
        if not name or not email or not password or not confirmPassword:
            return jsonify({"error": "All fields required"}), 400

        if users.find_one({'email': email}):
            return jsonify({"error": "User already exists"}), 409

        if password != confirmPassword:
            return jsonify({"error": "Password and confirm password does not match"}), 409

        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')

        users.insert_one({
            "username": name,
            "email": email,
            "password": hashed_pw,
            "image": None,
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow(),
            "refreshToken": None
        })

        access_token = create_access_token(identity=email)
        refresh_token = create_refresh_token(identity=email)

        users.update_one({"email": email}, {"$set": {"refreshToken": refresh_token}})

        return jsonify({
            "message": "Signup successful",
            "email": email,
            "access_token": access_token,
            "refresh_token": refresh_token
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =======================
# 🔹 Normal Login
# =======================
#@app.route('/login', methods=['POST'])
def normal_login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    user = users.find_one({'email': email})
    if not user:
        return jsonify({"error": "User not found"}), 404

    if not user.get("password"):
        return jsonify({"error": "Use Google login for this account"}), 400

    if not bcrypt.check_password_hash(user['password'], password):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=email)
    refresh_token = create_refresh_token(identity=email)
    users.update_one({"email": email}, {"$set": {"refreshToken": refresh_token}})

    return jsonify({
        "message": "Login successful",
        "email": email,
        "access_token": access_token,
        "refresh_token": refresh_token
    }), 200


# if __name__== '__main__':
#     app.run(host='0.0.0.0', port=5000,debug=True)