#!/usr/bin/python3
"""hold class Category"""

from course_hub.course import course_views
from flask import jsonify, abort, request
from models import storage
from models.category import Category
from flasgger.utils import swag_from
from course_hub.course.views import course_service
from marshmallow import ValidationError
from course_hub.course.schemas.category_schema import CreateCategorySchema
from course_hub.course.schemas.category_schema import UpdateCategorySchema
from course_hub.course.schemas.category_schema import CategorySchema


@course_views.route('/categories', methods=['GET'])
@swag_from('../documentation/categories/all_categories.yml', methods=['GET'])
def get_categories():
    """reterive all categories from storage
    """
    return jsonify(list(map(lambda category:
                            category.to_dict(), course_service.get_categories(
                                request.args.get('page', 1, type=int),
                                request.args.get('per_page', 3, type=int)
                            ))))


@course_views.route('/categories/<category_id>', methods=['GET'])
@swag_from('../documentation/categories/get_category.yml', methods=['GET'])
def get_category(category_id):
    """reterive category by id
    """
    category = storage.get(Category, category_id)
    if category is None:
        abort(404)
    return jsonify(category.to_dict())


@course_views.route('/categories/<category_id>/courses', methods=['GET'])
@swag_from('../documentation/categories/all_courses_category.yml', methods=['GET'])
def get_courses_category(category_id):
    """list all courses by category in storage"""
    category = storage.get(Category, category_id)
    if category is None:
        abort(404)

    return jsonify(list(map(lambda category:
                            category.to_dict(), course_service.get_courses_by_category(
                                category_id,
                                request.args.get('page', 1, type=int),
                                request.args.get('per_page', 3, type=int)
                            ))))
    # return jsonify([course.to_dict() for course in category.courses])


# admin permission
@course_views.route('/categories/<category_id>', methods=['DELETE'])
@swag_from('../documentation/categories/delete_category.yml', methods=['DELETE'])
def delete_category(category_id):
    """delete category by id
    """
    category = storage.get(Category, category_id)
    if category is None:
        abort(404)
    category.delete()
    storage.save()
    return jsonify({}), 200


# admin permission
@course_views.route('/categories', methods=['POST'])
@swag_from('../documentation/categories/post_category.yml', methods=['POST'])
def create_category():
    """post category to storage
    """
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    try:
        new_category = CreateCategorySchema().load(data)
    except ValidationError as err:
        return jsonify({'validation error': err.messages}), 422


    new_category.save()
    return jsonify(new_category.to_dict()), 201


# admin permission
@course_views.route('/categories/<category_id>', methods=['PUT'])
@swag_from('../documentation/categories/put_category.yml', methods=['PUT'])
def update_category(category_id):
    """update category to storage
    """
    category = storage.get(Category, category_id)
    if category is None:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    new_data = CategorySchema().dump(category)
    new_data.update(data)

    try:
        new_data['instance'] = category
        UpdateCategorySchema().load(new_data)
    except ValidationError as err:
        return jsonify({'validation error': err.messages}), 422

    category.save()
    return jsonify(category.to_dict()), 200
