from flask import Blueprint, Response, abort, jsonify, request
from database import db
import json
from bson.objectid import ObjectId

restaurant = Blueprint("restaurant", __name__)
restaurant_db = db.restaurant
menu_db = db.menu

@restaurant.route("/restaurant", methods=["GET"])
@restaurant.route("/restaurant/<id>", methods=["GET"])
def get_restaurant(id=None):
    restaurants = []
    if id is None:
        restaurants = restaurant_db.find({})
    elif ObjectId.is_valid(id):
        id = ObjectId(id)
        restaurants = restaurant_db.find({"_id": id})
    else:
        return {"message": "ID is not valid"}, 400
    resp = []
    for res in restaurants:
        resp.append({"_id": str(res["_id"]), "name": res["name"]})
    return jsonify(resp), 200

@restaurant.route("/restaurant", methods=["POST"])
def post_restaurant():
    request_body = request.get_json()
    name = request_body.get("name")
    if name is None:
        return {"message": "Cannot add restaurant as name is empty"}, 400
    rest_resp = restaurant_db.insert_one({"name": name})
    _ = menu_db.insert_one({"restaurant_id": rest_resp.inserted_id, "items": []})
    return {"_id": str(rest_resp.inserted_id)}, 200

@restaurant.route("/restaurant/<id>", methods=["PUT"])
def put_restaurant(id):
    request_body = request_body.get_json()
    name = request_body.get("name")
    if (name is None) or (id is None) or (not ObjectId.is_valid(id)):
        return {"message": "Provide valid name and valid ID of restaurant"}, 400
    resp = restaurant_db.find({"_id": ObjectId(id)})
    if not list(resp):
        return {"message": "ID of restaurant not found"}, 404
    restaurant_db.update_one({"_id": ObjectId(id)}, {"name": name})
    return {"_id": id}, 200

@restaurant.route("/restaurant/<id>", methods=["DELETE"])
def delete_restaurant(id):
    if not ObjectId.is_valid(id):
        return {"message": "Provide a valid ID of the restaurant"}, 400
    resp = restaurant_db.find({"_id": ObjectId(id)})
    if not list(resp):
        return {"message": "ID not found"}, 404
    restaurant_db.delete_one({"_id": ObjectId(id)})
    return {"message": "Successfully deleted"}, 200
