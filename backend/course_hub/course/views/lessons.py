#!/usr/bin/python3
"""new view for Course objects that handles all default RESTFul API actions"""

from course_hub.course import course_views
from flask import jsonify, abort, request
from models import storage
from models.course import Course
from models.section import Section
from models.lesson import Lesson
from flasgger.utils import swag_from




@course_views.route('/sections/<section_id>/lessons', methods=['GET'])
def get_lesson_section(section_id):
    """list all lessons by section in storage"""
    section = storage.get(Section, section_id)
    if section is None:
        abort(404)

    return jsonify([lesson.to_dict() for lesson in section.lessons])


@course_views.route('/lessons/<lesson_id>', methods=['GET'])
# @swag_from('documentation/user/get_user.yml', methods=['GET'])
def get_lesson(lesson_id):
    """reterive lesson by id
    """
    lesson = storage.get(Lesson, lesson_id)
    if lesson is None:
        abort(404)
    return jsonify(lesson.to_dict())


@course_views.route('/lessons/<lesson_id>', methods=['DELETE'])
# @swag_from('documentation/user/delete_user.yml', methods=['DELETE'])
def delete_lesson(lesson_id):
    """delete lesson by id
    """
    lesson = storage.get(Lesson, lesson_id)
    if lesson is None:
        abort(404)
    lesson.delete()
    storage.save()
    return jsonify({}), 200


@course_views.route('/sections/<section_id>/lessons', methods=['POST'])
# @swag_from('documentation/user/post_user.yml', methods=['POST'])
def create_lesson(section_id):
    """post lesson to storage
    """
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    if not data.get('name'):
        abort(400, "Missing name")

    lesson = Lesson(**data)
    lesson.section_id = section_id
    lesson.save()
    return jsonify(lesson.to_dict()), 201


@course_views.route('/lesson/<lesson_id>', methods=['PUT'])
# @swag_from('documentation/user/put_user.yml', methods=['PUT'])
def update_lesson(lesson_id):
    """update lesson to storage
    """
    lesson = storage.get(Lesson, lesson_id)
    if not lesson:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')

    for k, v in data.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(lesson, k, v)

    lesson.save()
    return jsonify(lesson.to_dict())
