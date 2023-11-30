#!/usr/bin/python3
"""new view for Course objects that handles all default RESTFul API actions"""

from course_hub.course import course_views
from flask import jsonify, abort, request
from models import storage
from models.section import Section
from models.lesson import Lesson
from flasgger.utils import swag_from
from course_hub.course.views import course_service
from marshmallow import ValidationError
from course_hub.course.schemas.lesson_schema import LessonSchema
from course_hub.course.schemas.lesson_schema import CreateLessonSchema
from course_hub.course.schemas.lesson_schema import UpdateLessonSchema


@course_views.route('/sections/<section_id>/lessons', methods=['GET'])
@swag_from('../documentation/lessons/all_lessons_section.yml', methods=['GET'])
def get_lesson_section(section_id):
    """list all lessons by section in storage"""
    section = storage.get(Section, section_id)
    if section is None:
        abort(404)

    return jsonify(list(map(lambda lesson:
                            lesson.to_dict(),
                            course_service.get_lessons_by_section(
                                section_id,
                                request.args.get('page', 1, type=int),
                                request.args.get('per_page', 3, type=int)
                            ))))
    # return jsonify([lesson.to_dict() for lesson in section.lessons])


@course_views.route('/lessons/<lesson_id>', methods=['GET'])
@swag_from('../documentation/lessons/get_lesson.yml', methods=['GET'])
def get_lesson(lesson_id):
    """reterive lesson by id
    """
    lesson = storage.get(Lesson, lesson_id)
    if lesson is None:
        abort(404)
    return jsonify(lesson.to_dict())


# admin permission or instructor of this course permission
@course_views.route('/lessons/<lesson_id>', methods=['DELETE'])
@swag_from('../documentation/lessons/delete_lesson.yml', methods=['DELETE'])
def delete_lesson(lesson_id):
    """delete lesson by id
    """
    lesson = storage.get(Lesson, lesson_id)
    if lesson is None:
        abort(404)
    lesson.delete()
    storage.save()
    return jsonify({}), 200


# admin permission or instructor of this course permission
@course_views.route('/sections/<section_id>/lessons', methods=['POST'])
@swag_from('../documentation/lessons/post_lesson.yml', methods=['POST'])
def create_lesson(section_id):
    """post lesson to storage
    """
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    if not data.get('section_id'):
        data['section_id'] = section_id

    try:
        new_lesson = CreateLessonSchema(context={'data': data}).load(data)
    except ValidationError as err:
        return jsonify({'validation error': err.messages}), 422

    new_lesson.save()
    return jsonify(new_lesson.to_dict()), 201


# admin permission or instructor of this course permission
@course_views.route('/lesson/<lesson_id>', methods=['PUT'])
@swag_from('../documentation/lessons/put_lesson.yml', methods=['PUT'])
def update_lesson(lesson_id):
    """update lesson to storage
    """
    lesson = storage.get(Lesson, lesson_id)
    if not lesson:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')

    new_data = LessonSchema().dump(lesson)
    new_data.update(data)

    try:
        lesson = UpdateLessonSchema(context={
            'data': new_data, 'instance': lesson
            }).load(new_data)
    except ValidationError as err:
        return jsonify({'validation error': err.messages}), 422

    lesson.save()
    return jsonify(lesson.to_dict())
