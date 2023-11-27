#!/usr/bin/python3
"""new view for Course objects that handles all default RESTFul API actions"""

from course_hub.course import course_views
from flask import jsonify, abort, request
from models import storage
from models.course import Course
from models.section import Section
from flasgger.utils import swag_from
from course_hub.course.views import course_service
from marshmallow import ValidationError
from course_hub.course.schemas.section_schema import SectionSchema
from course_hub.course.schemas.section_schema import CreateSectionSchema
from course_hub.course.schemas.section_schema import UpdateSectionSchema


@course_views.route('/courses/<course_id>/sections', methods=['GET'])
@swag_from('../documentation/sections/all_sections_course.yml', methods=['GET'])
def get_section_course(course_id):
    """list all section by course in storage"""
    course = storage.get(Course, course_id)
    if course is None:
        abort(404)

    return jsonify(list(map(lambda section:
                            section.to_dict(),
                            course_service.get_sections_by_course(
                                course_id,
                                request.args.get('page', 1, type=int),
                                request.args.get('per_page', 3, type=int)
                            ))))
    # return jsonify([section.to_dict() for section in course.sections])


@course_views.route('/sections/<section_id>', methods=['GET'])
@swag_from('../documentation/sections/get_section.yml', methods=['GET'])
def get_section(section_id):
    """reterive section by id
    """
    section = storage.get(Section, section_id)
    if section is None:
        abort(404)
    return jsonify(section.to_dict())


# admin permission or instructor of this course permission
@course_views.route('/sections/<section_id>', methods=['DELETE'])
@swag_from('../documentation/sections/delete_section.yml', methods=['DELETE'])
def delete_section(section_id):
    """delete Course by id
    """
    section = storage.get(Section, section_id)
    if section is None:
        abort(404)
    section.delete()
    storage.save()
    return jsonify({}), 200


# admin permission or instructor of this course permission
@course_views.route('/courses/<course_id>/sections', methods=['POST'])
@swag_from('../documentation/sections/post_section.yml', methods=['POST'])
def create_section(course_id):
    """post section to storage
    """
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    if not data.get('course_id'):
        data['course_id'] = course_id

    try:
        new_section = CreateSectionSchema().load(data)
    except ValidationError as err:
        return jsonify({'validation_error': err.messages}), 422

    new_section.save()
    return jsonify(new_section.to_dict()), 201


# admin permission or instructor of this course permission
@course_views.route('/sections/<section_id>', methods=['PUT'])
@swag_from('../documentation/sections/put_section.yml', methods=['PUT'])
def update_section(section_id):
    """update section to storage
    """
    section = storage.get(Section, section_id)
    if not section:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')

    new_data = SectionSchema().dump(section)
    new_data.update(data)

    try:
        new_data['instance'] = section
        UpdateSectionSchema().load(new_data)
    except ValidationError as err:
        return jsonify({'validation_error': err.messages}), 422

    section.save()
    return jsonify(section.to_dict())
