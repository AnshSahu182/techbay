from flask_cors import CORS
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
import os
from pymongo import MongoClient
from datetime import timedelta

from signup import normal_signup,normal_login,google_signup,google_login,callback
from home import show_categories,featured_products
from product import products_page,get_by_brand,get_by_category,get_by_price,single_product
from authentication import token_required
from profile import user_details,upload_profile_photo,add_address,view_address,delete_address,update_address,logout
from cart import view_cart,add_to_cart,delete_from_cart,reduce_from_cart
from wishlist import delete_from_wishlist,add_to_wishlist,view_wishlist
from order import confirm_order, view_orders, cancel_order

app=Flask(__name__)
CORS(app, supports_credentials=True)

# Set secret key for JWT
app.config["SECRET_KEY"]=os.getenv("SECRET_KEY")
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=30)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

# Initialize extensions
bcrypt = Bcrypt(app)
bcrypt.init_app(app)
jwt = JWTManager(app)

# Connect MongoDB
client=MongoClient(os.getenv('MongoClient_URI'))
db=client["techbay"]
users = db["users"]

##### COMMON Pages Start #####
#SignUp Page

#Call back api
@app.route("/callback", methods=['GET'])
def callback_route():
    return callback()

## Normal Signup
@app.route('/signup', methods=['POST'])
def normal_signup_route():
    return normal_signup()

#Google Signup
@app.route('/googlesignup', methods=['GET'])
def google_signup_route():
    return google_signup()
  

#Login Page

## Normal Login
@app.route('/login', methods=['POST'])
def normal_login_route():  
    return normal_login() 

## Google Login
@app.route('/googlelogin', methods=['POST'])
def google_login_route():
    return google_login()

# #Home Page

@app.route("/", methods=['GET'])
def show_categories_route(): 
    return show_categories()
    

@app.route("/feature", methods=['GET'])
def featured_products_route():
    return featured_products()
    

# #Product Page

@app.route("/products", methods=['GET'])
def products_route():
    return products_page()

@app.route("/products/categories", methods=['POST'])
def get_by_category_route():
    return get_by_category()

@app.route("/products/brand", methods=['POST'])
def get_by_brand_route():
    return get_by_brand()

@app.route("/products/price_range", methods=["POST"])
def get_by_price_route():
    return get_by_price()

@app.route("/products/<string:product_id>", methods=['GET'])
def single_product_route(product_id):
    return single_product(product_id)

##### COMMON Pages End #####

##### PROTECTED pages Start #####

# Profile Page

@app.route("/viewprofile", methods=['GET'])
@token_required
def user_details_route(current_user):
    return user_details(current_user)

@app.route('/upload-profile-photo', methods=['POST'])
@token_required
def upload_profile_photo_route(current_user):
    return upload_profile_photo(current_user)

@app.route("/addaddress", methods=['POST'])
@token_required
def add_address_route(current_user):
    return add_address(current_user)

@app.route('/viewaddress', methods=['GET'])
@token_required
def view_address_route(current_user):
    return view_address(current_user)

@app.route('/deleteaddress', methods=['DELETE'])
@token_required
def delete_address_route(current_user):
    return delete_address(current_user)

@app.route('/updateaddress', methods=['PUT'])
@token_required
def update_address_route(current_user):
    return update_address(current_user)

# @app.route("/logout",methods=["POST"])
# def logout_route(current_user):
#     return logout(current_user)

# Cart Page

@app.route("/addtocart", methods=["POST"])
@token_required
def add_to_cart_route(current_user):
    return add_to_cart(current_user)
    
@app.route("/viewcart",methods=["GET"])
@token_required
def view_cart_route(current_user):
    return view_cart(current_user)
    
@app.route("/deletefromcart",methods=["DELETE"])
@token_required
def delete_from_cart_route(current_user):
    return delete_from_cart(current_user)
    
@app.route("/reducefromcart", methods=["POST"])
@token_required
def reduce_from_cart_route(current_user):
    return reduce_from_cart(current_user)

# # Wishlist Page

@app.route("/addtowishlist/<string:product_id>", methods=["POST"])
@token_required
def add_to_wishlist_route(current_user,product_id):
    return add_to_wishlist(current_user,product_id)
    

@app.route("/removefromwishlist/<string:product_id>", methods=["DELETE"])
@token_required
def delete_from_wishlist_route(current_user, product_id):
    return delete_from_wishlist(current_user, product_id)

    
@app.route("/viewwishlist",methods=["GET"])
@token_required
def view_wishlist_route(current_user):
    return view_wishlist(current_user)
    
#Order page
@app.route('/confirmorder', methods=['POST'])
@token_required
def confirm_order_route(current_user):
    return confirm_order(current_user)

@app.route('/vieworders', methods=['GET'])
@token_required
def view_orders_route(current_user):
    return view_orders(current_user)

@app.route('/cancelorder/<string:order_id>', methods=['DELETE'])
@token_required
def cancel_order_route(current_user, order_id):
    return cancel_order(current_user, order_id)

if __name__== '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    app.run(host='0.0.0.0', use_reloader=False, port=5000,debug=True)