from pymongo import MongoClient
from dotenv import load_dotenv
import os
from flask import Flask,request,jsonify
from bson import ObjectId

load_dotenv()

client=MongoClient(os.getenv('MongoClient_URI'))
db=client["techbay"]
products=db["products"]

limit = 12

#Product Page
# @app.route("/products", methods=['GET'])
def products_page():
    page = int(request.args.get("page", 1))
    skip = (page - 1) * limit

    products_list = list(products.find())
    for product in products_list:
            product['_id'] = str(product['_id'])
    return jsonify(products_list),200


# @app.route("/products/categories", methods=['POST'])
def get_by_category():
    data = request.get_json()
    category = data.get('category')
    # page = int(request.args.get("page", 1))
    # skip = (page - 1) * limit

    if not category:
        return jsonify({"error": "Category is required"}), 400

    category_list = list(products.find({"category": category}).limit(limit))
    for product in category_list:
        product["_id"] = str(product["_id"])

    return jsonify(category_list)

# @app.route("/products/brand", methods=['POST'])
def get_by_brand():
    data = request.get_json()
    brand = data.get('brand')
    # page = int(request.args.get("page", 1))
    # skip = (page - 1) * limit

    if not brand:
        return jsonify({"error": "Brand is required"}), 400

    product_list = list(products.find({"brand": brand}).limit(limit))
    for product in product_list:
        product["_id"] = str(product["_id"])

    return jsonify(product_list)

# Get by price
# @app.route("/products/price_range", methods=["POST"])
def get_by_price():
    data= request.get_json()
    min_price = float(data.get('min', 0))
    max_price = float(data.get('max', 5000))

    # page = int(request.args.get("page", 1))
    # skip = (page - 1) * limit

    query = {"price":{"$gte":min_price,"$lte":max_price}}
    products_list=list(products.find(query).limit(limit))

    for product in products_list:
        product['_id'] = str(product['_id'])
    return jsonify(products_list), 200

# @app.route("/products/<string:product_id>", methods=['GET'])
def single_product(product_id):
    try:
        product = products.find_one({"_id": ObjectId(product_id)})
        if not product:
            return jsonify({"error": "Product not found"}), 404

        product["_id"] = str(product["_id"])
        return jsonify(product), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    