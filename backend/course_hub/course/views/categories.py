#!/usr/bin/python3
"""hold class Category"""

from course_hub.course import course_views
from flask import jsonify, abort, request
from models import storage
from models.category import Category
from flasgger.utils import swag_from


@course_views.route('/categories', methods=['GET'])
# @swag_from('documentation/category/all_categories.yml')
def get_categories():
    """reterive all categories from storage
    """
    categories = storage.all(Category).values()
    return jsonify([category.to_dict() for category in categories])


@course_views.route('/categories/<category_id>', methods=['GET'])
# @swag_from('documentation/category/get_category')
def get_category(category_id):
    """reterive category by id
    """
    category = storage.get(Category, category_id)
    if category is None:
        abort(404)
    return jsonify(category.to_dict())


@course_views.route('/categories/<category_id>/courses', methods=['GET'])
def get_courses_category(category_id):
    """list all courses by category in storage"""
    category = storage.get(Category, category_id)
    if category is None:
        abort(404)

    return jsonify([course.to_dict() for course in category.courses])


@course_views.route('/categories/<category_id>', methods=['DELETE'])
def delete_category(category_id):
    """delete category by id
    """
    category = storage.get(Category, category_id)
    if category is None:
        abort(404)
    category.delete()
    storage.save()
    return jsonify({}), 200


@course_views.route('/categories', methods=['POST'])
# @swag_from('documentation/category/post_category')
def create_category():
    """post category to storage
    """
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    if not data.get('name'):
        abort(400, "Missing name")

    category = Category(**data)
    category.save()
    return jsonify(category.to_dict()), 201


@course_views.route('/categories/<category_id>', methods=['PUT'])
# @swag_from('documentation/category/put_category')
def update_category(category_id):
    """update category to storage
    """
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    category = storage.get(Category, category_id)
    if category is None:
        abort(404)

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(category, key, value)

    category.save()
    return jsonify(category.to_dict()), 200
