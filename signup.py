from flask import Flask,request,jsonify,redirect, url_for,session
from authlib.integrations.flask_client import OAuth # for login
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, create_refresh_token,JWTManager

load_dotenv()

app=Flask(__name__)
bcrypt=Bcrypt(app)
jwt = JWTManager(app)
app.secret_key=os.getenv('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
client=MongoClient(os.getenv('MongoClient_URI'))
db=client["TechbayDB"]
users=db["users"]

# 🔑 Google OAuth Configuration
oauth = OAuth(app)
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

@app.route('/')
def home():
    return "app running"

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = data['password']

    existing_user = users.find_one({"email": email})
    if existing_user:
        return jsonify({"message": "User already exists"}), 400

    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
    user_data = {
        "username": username,
        "email": email,
        "password": hashed_pw,
        "image": None,
        "refreshToken": None,
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    }
    users.insert_one(user_data)
    return jsonify({"message": "Signup successful!"}), 201

#Login
@app.route("/login", methods=['GET'])  
#data here does not goto server it goes to google and it send redirected url that is why there is GET 
def login():
    redirect_uri=url_for('callback',_external=True)
    return google.authorize_redirect(redirect_uri)

#Callback (Direct google login ka data deta h )
@app.route("/callback", methods=['GET'])
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
            {'email':email},{"$set":{"image":picture,"updatedAt":datetime.utcnow()}}
        )
    else:
        users.insert_one(new_user={
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

if __name__== '__main__':
    app.run(debug=True, port=5000)