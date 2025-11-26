from pymongo import MongoClient
from dotenv import load_dotenv
import os
from flask import Flask,request,jsonify
from flask_cors import CORS
from bson import ObjectId

load_dotenv()
app=Flask(__name__)
CORS(app)
client=MongoClient(os.getenv('MongoClient_URI'))
db=client["techbay"]
products=db["products"]
categories=db["categories"]

# Show Categories
@app.route("/", methods=['GET'])
def show_categories():
    category_list=list(categories.find({}))
    # Convert ObjectId to string
    for category in category_list:
        category['_id'] = str(category['_id'])
      
    return jsonify(category_list)

# Featured Products
@app.route("/feature", methods=['GET'])
def featured_products():
    featured_ids = [
        "65b54e14a39a3ffd12fd2c12",
        "65b54e14a39a3ffd12fd2c0e",
        "65b54e14a39a3ffd12fd2c0c",
        "65b54e15a39a3ffd12fd2c16"
    ]

    # Convert strings to ObjectIds
    object_ids = [ObjectId(pid) for pid in featured_ids]

    # Fetch only these products
    featured = list(products.find(
        {"_id": {"$in": object_ids}},
        {"_id": 1, "title": 1,"description":1, "price": 1, "image": 1, "category": 1}  # optional: limit fields
    ))

    # Convert ObjectIds to strings for JSON
    for prod in featured:
        prod["_id"] = str(prod["_id"])

    return jsonify(featured), 200


if __name__== '__main__':
    app.run(host='0.0.0.0', port=5001,debug=True)