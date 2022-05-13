from flask import Blueprint, Response, abort, jsonify, request
from database import db
import json
from bson.objectid import ObjectId

order = Blueprint("order", __name__)
order_db = db.order
menu_db = db.menu

@order.route("/order/<order_id>", methods=["GET"])
def get_order(order_id):
    if not ObjectId.is_valid(order_id):
        return {"message": "Provide a valid ID"}, 400
    orders = order_db.find({"_id": ObjectId(order_id)})
    resp = []
    for o in list(orders):
        resp.append({"_id": str(o["_id"]), "items": o["items"], "total": o["total"]})
    return jsonify(resp), 200

@order.route("/order", methods=["POST"])
def post_order():
    request_body = request.get_json()
    items = {}
    restaurant_id = request_body.get("restaurant_id")
    if not ObjectId.is_valid(restaurant_id):
        return {"message": "Provide valid ID"}, 400
    item_names = []
    for item in request_body.get("items", []):
        if item.get("name") and item.get("quantity"):
            items[item.get("name")] = item.get("quantity")
    item_names = list(items.keys())
    print(item_names)
    menu = menu_db.find(
        {"restaurant_id": ObjectId(restaurant_id)}, {"items": {"$elemMatch": {"name": {"$in": item_names}}}}
    )
    menu = list(menu)
    print("menu", menu)
    if (not menu) or (not menu[0].get("items")):
        return {"message": "Items not found in menu"}, 400
    menu_items = menu[0].get("items", [])
    total = 0
    for menu_item in menu_items:
        name = menu_item.get("name")
        quantity = items.get(name)
        total = total + (menu_item["price"]*quantity)
    resp = order_db.insert_one({"restaurant_id": ObjectId(restaurant_id), "items": items, "total": total})
    return {"_id": str(resp.inserted_id), "total": total}, 200