#!/usr/bin/python3
""" validation for class Course"""

from marshmallow import Schema, fields, validate, ValidationError, validates, post_load

from models import storage
from models.course import Course

from course_hub.course import course_service


class CourseSchema(Schema):

    name = fields.String(required=True)
    description = fields.String()
    hours = fields.Integer(required=True, validate=validate.Range(min=1))
    num_sections = fields.Integer(required=True, validate=validate.Range(min=1))
    num_enrolled = fields.Integer(validate=validate.Range(min=0))
    category_id = fields.String()
    instructor_id = fields.String(required=True)


    @post_load
    def make_course(self, data, **kwargs):
        return Course(**data)

    @validates('name')
    def validate_name(self, value):
        if len(value) < 3:
            raise ValidationError("Name cannot be less than 3 characters")

    @validates('category_id')
    def validate_category_id(self, value):
        if not course_service.get_category(value):
            raise ValidationError("Category doesn't exist")

    @validates('instructor_id')
    def validate_instructor_id(self, value):
        if not course_service.get_instructor(value):
            raise ValidationError("Instructor doesn't exist")
