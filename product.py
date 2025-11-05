from pymongo import MongoClient
from dotenv import load_dotenv
import os
from flask import Flask,request,jsonify
from flask_cors import CORS
import json
from bson import ObjectId

load_dotenv()
app=Flask(__name__)
CORS(app)
client=MongoClient(os.getenv('MongoClient_URI'))
db=client["TechbayDB"]
products=db["products"]

#Product Page
@app.route("/products", methods=['GET'])
def prodcuts():
    products_list=list(products.find())
    for product in products_list:
            product['_id'] = str(product['_id'])
    return (products_list),200

@app.route("/products/categories", methods=['POST'])
def get_by_category():
    data = request.get_json()
    category = data.get('category')

    if not category:
        return jsonify({"error": "Category is required"}), 400

    product_list = list(products.find({"category": category}, {"_id": 0}))
    return jsonify(product_list)

@app.route("/products/brand", methods=['POST'])
def get_by_brand():
    data = request.get_json()
    brand = data.get('brand')

    if not brand:
        return jsonify({"error": "Brand is required"}), 400

    product_list = list(products.find({"brand": brand}, {"_id": 0}))
    return jsonify(product_list)

@app.route("/products/price_range", methods=["POST"])
def get_by_price():
    data= request.get_json()
    min_price=data.get('min')
    max_price=data.get('max')
    query = {"price":{"$gte":min_price,"$lte":max_price}}
    products_list=list(products.find(query))

# Convert ObjectIds to string
    for product in products_list:
        product['_id'] = str(product['_id'])
    return jsonify(products_list), 200


if __name__== '__main__':
    app.run(host='0.0.0.0' ,debug=True, port=5002)