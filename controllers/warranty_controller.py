

from flask import request, jsonify
from db import db

from models.product import Products
from models.warranty import Warranties


def add_warranty():
    post_data = request.form if request.form else request.get_json()

    fields = ["product_id", "warranty_months"]
    required_fields = ["product_id", "warranty_months"]

    values = {}

    for field in fields:
        field_data = post_data.get(field)

        if field in required_fields and not field_data:
            return jsonify({"message": f"{field} is required"}), 400

        values[field] = field_data

    product = db.session.query(Products).filter(Products.product_id == values["product_id"]).first()
    if not product:
        return jsonify({"message": "product not found"}), 404

    new_warranty = Warranties(
        warranty_months=values["warranty_months"],
        product_id=values["product_id"]
    )

    db.session.add(new_warranty)

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create warranty"}), 400

    return jsonify({
        "message": "warranty created",
        "result": {
            "warranty_id": new_warranty.warranty_id,
            "product_id": new_warranty.product_id,
            "warranty_months": new_warranty.warranty_months
        }
    }), 201


def get_warranty_by_id(warranty_id):
    warranty = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()
    if not warranty:
        return jsonify({"message": "warranty not found"}), 404

    return jsonify({
        "message": "warranty found",
        "result": {
            "warranty_id": warranty.warranty_id,
            "product_id": warranty.product_id,
            "warranty_months": warranty.warranty_months
        }
    }), 200


def get_all_warranties():
    query = db.session.query(Warranties).all()

    results = []
    for w in query:
        results.append({
            "warranty_id": w.warranty_id,
            "product_id": w.product_id,
            "warranty_months": w.warranty_months
        })

    return jsonify({"message": "warranties found", "results": results}), 200


def update_warranty_by_id(warranty_id):
    warranty = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()
    if not warranty:
        return jsonify({"message": "warranty not found"}), 404

    post_data = request.form if request.form else request.get_json()

    if "warranty_months" in post_data:
        warranty.warranty_months = post_data["warranty_months"]

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to update warranty"}), 400

    return jsonify({
        "message": "warranty updated",
        "result": {
            "warranty_id": warranty.warranty_id,
            "product_id": warranty.product_id,
            "warranty_months": warranty.warranty_months
        }
    }), 200


def delete_warranty(warranty_id):
    warranty = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()
    if not warranty:
        return jsonify({"message": "warranty not found"}), 404

    db.session.delete(warranty)

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete warranty"}), 400

    return jsonify({
        "message": "warranty deleted",
        "result": {
            "warranty_id": warranty.warranty_id,
            "product_id": warranty.product_id,
            "warranty_months": warranty.warranty_months
        }
    }), 200