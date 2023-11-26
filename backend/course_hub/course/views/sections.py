#!/usr/bin/python3
"""new view for Course objects that handles all default RESTFul API actions"""

from course_hub.course import course_views
from flask import jsonify, abort, request
from models import storage
from models.course import Course
from models.section import Section
from flasgger.utils import swag_from
from course_hub.course import course_service


@course_views.route('/courses/<course_id>/sections', methods=['GET'])
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
# @swag_from('documentation/user/get_user.yml', methods=['GET'])
def get_section(section_id):
    """reterive section by id
    """
    section = storage.get(Section, section_id)
    if section is None:
        abort(404)
    return jsonify(section.to_dict())


@course_views.route('/sections/<section_id>', methods=['DELETE'])
# @swag_from('documentation/user/delete_user.yml', methods=['DELETE'])
def delete_section(section_id):
    """delete Course by id
    """
    section = storage.get(Section, section_id)
    if section is None:
        abort(404)
    section.delete()
    storage.save()
    return jsonify({}), 200


@course_views.route('/courses/<course_id>/sections', methods=['POST'])
# @swag_from('documentation/user/post_user.yml', methods=['POST'])
def create_section(course_id):
    """post section to storage
    """
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    if not data.get('name'):
        abort(400, "Missing name")

    section = Section(**data)
    section.course_id = course_id
    section.save()
    return jsonify(section.to_dict()), 201


@course_views.route('/sections/<section_id>', methods=['PUT'])
# @swag_from('documentation/user/put_user.yml', methods=['PUT'])
def update_section(section_id):
    """update section to storage
    """
    section = storage.get(Section, section_id)
    if not section:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')

    for k, v in data.items():
        if k not in ['id', 'created_at', 'updated_at', 'course_id']:
            setattr(section, k, v)

    section.save()
    return jsonify(section.to_dict())
