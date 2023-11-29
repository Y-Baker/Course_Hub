#!/usr/bin/python3
""" validation for class Course"""

from marshmallow import Schema, fields, INCLUDE, post_load
from marshmallow import validate, validates, ValidationError

from models import storage
from models.course import Course
from models.instructor import Instructor
from models.category import Category



class CourseSchema(Schema):
    class Meta:
        unknown = INCLUDE
    name = fields.String(required=True)
    description = fields.String()
    hours = fields.Integer(required=True, validate=validate.Range(min=1))
    num_sections = fields.Integer(required=True, validate=validate.Range(min=1))
    num_enrolled = fields.Integer(validate=validate.Range(min=0))
    category_id = fields.String()
    instructor_id = fields.String(required=True)


    @validates('name')
    def validate_name(self, value):
        if len(value) < 3:
            raise ValidationError("Name cannot be less than 3 characters")

    @validates('category_id')
    def validate_category_id(self, value):
        if not storage.get(Category, value):
            raise ValidationError("Category doesn't exist")

    @validates('instructor_id')
    def validate_instructor_id(self, value):
        if not storage.get(Instructor, value):
            raise ValidationError("Instructor doesn't exist")

    @validates('num_sections')
    def validate_num_sections(self, value):
        course = self.context.get('instance', None)
        if course:
            if value < len(course.sections):
                raise ValidationError("num_sections cannot be less\
                                      than the number of sections exists")

class CreateCourseSchema(CourseSchema):
    @post_load
    def make_course(self, data, **kwargs):
        return Course(**data)


class UpdateCourseSchema(CourseSchema):
    @post_load
    def update_course(self, data, **kwargs):
        course = self.context.get('instance', None)
        if course:
            for key, value in data.items():
                if key not in ['id', 'created_at', 'updated_at', 'instractor_id']:
                    setattr(course, key, value)
        return course
