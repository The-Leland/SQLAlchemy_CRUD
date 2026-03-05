from flask import request, jsonify
import uuid
from db import db

from models.product import Products
from models.product_categories import Categories


def get_product_by_id(product_id):
    product = db.session.query(Products).filter(Products.product_id == product_id).first()
    if not product:
        return jsonify({"message": f"product does not exist"}), 400

    print(product)

    company_dict = {
        'company_id': product.company.company_id,
        'company_name': product.company.company_name
    }

    if product.warranty:
        warranty_dict = {
            'warranty_id': product.warranty.warranty_id,
            'warranty_months': product.warranty.warranty_months
        }
    else:
        warranty_dict = {}

    category_list = []
    for c in product.categories:
        category_list.append({
            "category_id": c.category_id,
            "category_name": c.category_name
        })

    product_dict = {
        'product_id': product.product_id,
        'product_name': product.product_name,
        'description': product.description,
        'price': product.price,
        'active': product.active,
        'company': company_dict,
        'warranty': warranty_dict,
        'categories': category_list
    }

    return jsonify({"message": "product found", "results": product_dict}), 200

def get_all_products():
    query = db.session.query(Products).all()

    product_list = []

    for product in query:
        company_dict = {
            "company_id": product.company.company_id,
            "company_name": product.company.company_name
        }

        if product.warranty:
            warranty_dict = {
                "warranty_id": product.warranty.warranty_id,
                "warranty_months": product.warranty.warranty_months
            }
        else:
            warranty_dict = {}

        category_list = []
        for c in product.categories:
            category_list.append({
                "category_id": c.category_id,
                "category_name": c.category_name
            })

        product_dictionary = {
            "product_id": product.product_id,
            "product_name": product.product_name,
            "description": product.description,
            "price": product.price,
            "active": product.active,
            "company": company_dict,
            "warranty": warranty_dict,
            "categories": category_list
        }

        product_list.append(product_dictionary)

    return jsonify({"message": "products found", "results": product_list}), 200


def add_product():
    post_data = request.form if request.form else request.get_json()

    fields = ["company_id", "product_name", "description", "price", "active"]
    required_fields = ["company_id", "product_name", "price"]

    values = {}

    for field in fields:
        field_data = post_data.get(field)

        if field in required_fields and not field_data:
            return jsonify({"message": f"{field} is required"}), 400

        values[field] = field_data

    
    try:
        company_uuid = uuid.UUID(values["company_id"])
    except:
        return jsonify({"message": "invalid company_id format"}), 400

    new_product = Products(
        company_uuid,
        values["product_name"],
        values.get("description"),
        values["price"],
        values.get("active", True)
    )

    try:
        db.session.add(new_product)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print("ERROR:", e)  
        return jsonify({"message": "unable to create product"}), 400

    product = {
        "product_id": new_product.product_id,
        "product_name": new_product.product_name,
        "description": new_product.description,
        "price": new_product.price,
        "active": new_product.active,
        "company_id": new_product.company_id
    }

    return jsonify({"message": "product created", "result": product}), 201



def update_product_by_id(product_id):
    post_data = request.form if request.form else request.get_json()

    query = db.session.query(Products).filter(Products.product_id == product_id).first()

    if not query:
        return jsonify({"message": "product not found"}), 404

    query.product_name = post_data.get("product_name", query.product_name)
    query.description = post_data.get("description", query.description)
    query.price = post_data.get("price", query.price)
    query.active = post_data.get("active", query.active)
    query.company_id = post_data.get("company_id", query.company_id)

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to update product"}), 400

    updated = db.session.query(Products).filter(Products.product_id == product_id).first()

    product = {
        "product_id": updated.product_id,
        "product_name": updated.product_name,
        "description": updated.description,
        "price": updated.price,
        "active": updated.active,
        "company_id": updated.company_id
    }

    return jsonify({"message": "product updated", "results": product}), 200


def delete_product_by_id(product_id):
    query = db.session.query(Products).filter(Products.product_id == product_id).first()

    if not query:
        return jsonify({"message": "product not found"}), 404

    try:
        db.session.delete(query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete product"}), 400

    return jsonify({"message": "product deleted", "product_id": product_id}), 200


