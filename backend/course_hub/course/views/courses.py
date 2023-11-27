#!/usr/bin/python3
"""new view for Course objects that handles all default RESTFul API actions"""

from course_hub.course import course_views
from flask import jsonify, abort, request
from models import storage
from models.course import Course
from models.instructor import Instructor
from flasgger.utils import swag_from
from course_hub.course.views import course_service



@course_views.route('/courses', methods=['GET'])
@swag_from('../documentation/courses/all_courses.yml', methods=['GET'])
def get_courses():
    """reterive all courses from storage
    """
    return jsonify(list(map(lambda course:
                            course.to_dict(), course_service.get_courses(
                                request.args.get("page", 1, type=int),
                                request.args.get("per_page", 3, type=int)
                            ))))


@course_views.route('/instructors/<instructor_id>/courses', methods=['GET'])
def get_courses_instructor(instructor_id):
    """list all courses by instructor in storage"""
    instructor = storage.get(Instructor, instructor_id)
    if instructor is None:
        abort(404)

    return jsonify(list(map(lambda course:
                            course.to_dict(), course_service.get_courses_by_instructor(
                                instructor_id,
                                request.args.get("page", 1, type=int),
                                request.args.get("per_page", 3, type=int)
                                ))))
    # return jsonify([course.to_dict() for course in instructor.courses])


@course_views.route('/courses/<course_id>', methods=['GET'])
@swag_from('../documentation/courses/get_course.yml', methods=['GET'])
def get_course(course_id):
    """reterive course by id
    """
    course = storage.get(Course, course_id)
    if course is None:
        abort(404)
    return jsonify(course.to_dict())


@course_views.route('/courses/<course_id>', methods=['DELETE'])
@swag_from('../documentation/courses/delete_course.yml', methods=['DELETE'])
def delete_course(course_id):
    """delete Course by id
    """
    course = storage.get(Course, course_id)
    if course is None:
        abort(404)
    course.delete()
    storage.save()
    return jsonify({}), 200


@course_views.route('/instructors/<instructor_id>/courses', methods=['POST'])
@swag_from('../documentation/courses/post_course.yml', methods=['POST'])
def create_course(instructor_id):
    """post course to storage
    """
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    if not data.get('name'):
        abort(400, "Missing name")

    if not data.get('hours'):
        abort(400, "Missing hours")


    course = Course(**data)
    course.instructor_id = instructor_id
    course.save()
    return jsonify(course.to_dict()), 201


@course_views.route('/courses/<course_id>', methods=['PUT'])
@swag_from('../documentation/courses/put_course.yml', methods=['PUT'])
def update_user(course_id):
    """update Course to storage
    """
    cousre = storage.get(Course, course_id)
    if not cousre:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')

    for k, v in data.items():
        if k not in ['id', 'created_at', 'updated_at', 'instractor_id']:
            setattr(cousre, k, v)

    cousre.save()
    return jsonify(cousre.to_dict())
