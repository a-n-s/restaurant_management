from flask import Blueprint, Response, abort, jsonify, request
from database import db
from bson.objectid import ObjectId
from pymongo import ReturnDocument

menu = Blueprint("menu", __name__)
restaurant_db = db.restaurant
menu_db = db.menu

@menu.route("/restaurant/<id>/menu", methods=["GET"])
def get_menu(id):
    if not ObjectId.is_valid(id):
        return {"message": "Provide a valid ID"}, 400
    menu = menu_db.find({"restaurant_id": ObjectId(id)})
    resp = []
    for m in menu:
        resp.append({"_id": str(m["_id"]), "items": m["items"]})
    return jsonify(resp), 200

@menu.route("/restaurant/<id>/menu", methods=["POST"])
def post_menu(id):
    if not ObjectId.is_valid(id):
        return {"message": "Provide a vaid ID"}, 400
    request_body = request.get_json()
    udpated_items = []
    for item in request_body.get("items", []):
        if item.get("name") and item.get("price"):
            udpated_items.append({"name": item.get("name"), "price": item.get("price")})
    resp = menu_db.find_one_and_update({"restaurant_id": ObjectId(id)}, {"$set": {
        "items": udpated_items
    }}, return_document=ReturnDocument.AFTER)
    return {"_id": str(resp["_id"]), "items": resp["items"]}, 200
