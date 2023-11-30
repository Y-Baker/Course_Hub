#!/usr/bin/python3
"""new view for Course objects that handles all default RESTFul API actions"""

from course_hub.course import course_views
from flask import jsonify, abort, request
from models import storage
from models.course import Course
from models.instructor import Instructor
from flasgger.utils import swag_from
from course_hub.course.views import course_service
from course_hub.course.schemas.course_schema import CourseSchema
from course_hub.course.schemas.course_schema import CreateCourseSchema, UpdateCourseSchema
from marshmallow import ValidationError
from flask_jwt_extended import current_user, jwt_required
from utils.auth_utils import user_required

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
@swag_from('../documentation/courses/all_courses_instructor.yml', methods=['GET'])
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


# admin permission or instructor of this course permission
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


# admin permission or instructor permission
@course_views.route('/instructors/<instructor_id>/courses', methods=['POST'])
@jwt_required()
@user_required([1])
@swag_from('../documentation/courses/post_course.yml', methods=['POST'])
def create_course(instructor_id):
    """post course to storage
    """
    data = request.get_json()
    if current_user.id != instructor_id:
        abort(403)
    if not data:
        abort(400, "Not a JSON")
    if not data.get('instructor_id'):
        data['instructor_id'] = instructor_id
    createCourseSchema = CreateCourseSchema()
    try:
        new_course = CreateCourseSchema(context={'data': data}).load(data)
    except ValidationError as err:
        return jsonify({'validation_error': err.messages}), 422
    print("before")
    print(new_course)
    new_course.save()
    return jsonify({
        "message" : "success",
        "data": createCourseSchema.dump(new_course)    
    }), 201


# admin permission or instructor of this course permission
@course_views.route('/courses/<course_id>', methods=['PUT'])
@swag_from('../documentation/courses/put_course.yml', methods=['PUT'])
def update_user(course_id):
    """update Course to storage
    """
    course = storage.get(Course, course_id)
    if not course:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')

    new_data = CourseSchema().dump(course)
    new_data.update(data)
    try:
        UpdateCourseSchema(context={
            'data': new_data, 'instance': course
        }).load(new_data)
    except ValidationError as err:
        return jsonify({'validation_error': err.messages}), 422

    course.save()
    return jsonify(course.to_dict())
