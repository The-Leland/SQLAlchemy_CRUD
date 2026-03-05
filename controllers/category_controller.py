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
        if field_data in required_fields and not field_data:
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