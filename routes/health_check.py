from flask import Blueprint, request, jsonify
from database.db import db
from sqlalchemy import text


health_bp = Blueprint("health", __name__)

@health_bp.route("/health/live", methods=["GET"])
def liveness():
    return jsonify({
        "status": "UP"
    }), 200

@health_bp.route("/health/ready", methods=["GET"])
def readiness():

    try:
        db.session.execute(text("SELECT 1"))

        return jsonify({
            "status": "READY"
        }), 200

    except Exception as ex:

        return jsonify({
            "status": "NOT_READY"
        }), 503