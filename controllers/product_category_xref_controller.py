


from flask import request, jsonify
from db import db

from models.product import Products
from models.product_categories import Categories
from models.product_category_xref import products_categories_association_table


def add_category_to_product():
    post_data = request.form if request.form else request.get_json()

    fields = ["product_id", "category_id"]
    required_fields = ["product_id", "category_id"]

    values = {}

    for field in fields:
        field_data = post_data.get(field)

        if field in required_fields and not field_data:
            return jsonify({"message": f"{field} is required"}), 400

        values[field] = field_data

    product = db.session.query(Products).filter(Products.product_id == values["product_id"]).first()
    if not product:
        return jsonify({"message": "product not found"}), 404

    category = db.session.query(Categories).filter(Categories.category_id == values["category_id"]).first()
    if not category:
        return jsonify({"message": "category not found"}), 404

    if category in product.categories:
        return jsonify({"message": "category already assigned to product"}), 400

    product.categories.append(category)

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to assign category"}), 400

    return jsonify({"message": "category added to product"}), 201


def remove_category_from_product():
    post_data = request.form if request.form else request.get_json()

    fields = ["product_id", "category_id"]
    required_fields = ["product_id", "category_id"]

    values = {}

    for field in fields:
        field_data = post_data.get(field)

        if field in required_fields and not field_data:
            return jsonify({"message": f"{field} is required"}), 400

        values[field] = field_data

    product = db.session.query(Products).filter(Products.product_id == values["product_id"]).first()
    if not product:
        return jsonify({"message": "product not found"}), 404

    category = db.session.query(Categories).filter(Categories.category_id == values["category_id"]).first()
    if not category:
        return jsonify({"message": "category not found"}), 404

    if category not in product.categories:
        return jsonify({"message": "category not assigned to product"}), 400

    product.categories.remove(category)

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to remove category"}), 400

    return jsonify({"message": "category removed from product"}), 200


def get_all_product_categories():
    query = db.session.query(products_categories_association_table).all()

    results = []
    for row in query:
        results.append({
            "product_id": row.product_id,
            "category_id": row.category_id
        })

    return jsonify({"message": "product categories found", "results": results}), 200


def get_product_category():
    post_data = request.form if request.form else request.get_json()

    fields = ["product_id", "category_id"]
    required_fields = ["product_id", "category_id"]

    values = {}

    for field in fields:
        field_data = post_data.get(field)

        if field in required_fields and not field_data:
            return jsonify({"message": f"{field} is required"}), 400

        values[field] = field_data

    query = db.session.query(products_categories_association_table).filter(
        products_categories_association_table.c.product_id == values["product_id"],
        products_categories_association_table.c.category_id == values["category_id"]
    ).first()

    if not query:
        return jsonify({"message": "product/category pair not found"}), 404

    result = {
        "product_id": query.product_id,
        "category_id": query.category_id
    }

    return jsonify({"message": "product category found", "result": result}), 200