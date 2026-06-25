from flask import Blueprint, request, jsonify
from services.user_service import *

user_bp = Blueprint("user", __name__)

@user_bp.route("/users",methods=["GET"])
def get_users():
    return jsonify(get_all_users())

@user_bp.route("/users/<uid>", methods=["GET"])
def get_user_by_uid(uid):
    user = get_user(uid)

    if not user:
        return jsonify({"error": "Not Found"}), 404

    return jsonify(user)

@user_bp.route("/users", methods=["POST"])
def create_user_details():
    user_data = request.get_json()

    user = create_user(
        uid = user_data.get("uid"),
        name = user_data["name"],
        email = user_data["email"]
    )

    return jsonify(user), 201

@user_bp.route("/users/<uid>", methods = ["PUT"])
def update_user_details(uid):
    data = request.get_json()

    user = update_user(
        uid = uid,
        name = data.get("name"),
        email = data.get("email")
    )

    if not user:
        return jsonify({"error" : "User not found"}),404
    return jsonify(user)

@user_bp.route("/users/<uid>", methods=["DELETE"])
def delete_user_details(uid):
    user = delete_user(uid=uid)

    if not user:
        return jsonify({"error": "User not found"}),404
    return user
