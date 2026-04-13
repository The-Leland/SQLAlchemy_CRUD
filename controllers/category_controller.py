from flask import request, jsonify

from db import db
from models.product_categories import Categories


def add_category():
    post_data = request.form if request.form else request.get_json()

    fields = ['category_name']
    required_fields = ['category_name']

    values = {}

    for field in fields:
        field_data = post_data.get(field)
        if field in required_fields and not field_data:
            return jsonify({"message": f'{field} is required'}), 400

        values[field] = field_data

    new_category = Categories(values['category_name'])

    try:
        db.session.add(new_category)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create record"}), 400

    query = db.session.query(Categories).filter(Categories.category_name == values['category_name']).first()

    values['category_id'] = query.category_id

    return jsonify({"message": "category created", "result": values}), 201


def get_all_categories():
    query = db.session.query(Categories).all()

    results = []
    for c in query:
        results.append({
            "category_id": c.category_id,
            "category_name": c.category_name
        })

    return jsonify({"message": "categories found", "results": results}), 200


def get_category_by_id(category_id):
    query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if not query:
        return jsonify({"message": "category not found"}), 404

    result = {
        "category_id": query.category_id,
        "category_name": query.category_name
    }

    return jsonify({"message": "category found", "result": result}), 200


def update_category():
    post_data = request.form if request.form else request.get_json()

    category_id = post_data.get("category_id")
    if not category_id:
        return jsonify({"message": "category_id is required"}), 400

    query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if not query:
        return jsonify({"message": "category not found"}), 404

    query.category_name = post_data.get("category_name", query.category_name)

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to update record"}), 400

    updated = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    result = {
        "category_id": updated.category_id,
        "category_name": updated.category_name
    }

    return jsonify({"message": "category updated", "result": result}), 200


def delete_category():
    post_data = request.form if request.form else request.get_json()

    category_id = post_data.get("category_id")
    if not category_id:
        return jsonify({"message": "category_id is required"}), 400

    query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if not query:
        return jsonify({"message": "category not found"}), 404

    try:
        db.session.delete(query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete record"}), 400

    return jsonify({
        "message": "category deleted",
        "result": {
            "category_id": category_id
        }
    }), 200

