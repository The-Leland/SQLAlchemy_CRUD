from flask import Blueprint
import controllers

product_category_xref = Blueprint("product_category_xref", __name__)

@product_category_xref.route('/product-category', methods=['POST'])
def add_category_to_product():
    return controllers.add_category_to_product()

@product_category_xref.route('/product-category', methods=['DELETE'])
def remove_category_from_product():
    return controllers.remove_category_from_product()

@product_category_xref.route('/product-categories', methods=['GET'])
def get_all_product_categories():
    return controllers.get_all_product_categories()

@product_category_xref.route('/product-category/get', methods=['POST'])
def get_product_category():
    return controllers.get_product_category()

