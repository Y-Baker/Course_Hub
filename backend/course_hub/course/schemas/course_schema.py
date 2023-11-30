#!/usr/bin/python3
""" validation for class Course"""

from marshmallow import Schema, fields, INCLUDE, post_load
from marshmallow import validate, validates, ValidationError

from models import storage
from models.course import Course
from models.instructor import Instructor
from models.category import Category
from models.lesson import Lesson
from models.section import Section



class CourseSchema(Schema):
    class Meta:
        unknown = INCLUDE
    name = fields.String(required=True)
    description = fields.String()
    hours = fields.Integer(required=True, validate=validate.Range(min=1))
    num_sections = fields.Integer(required=True, validate=validate.Range(min=1))
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

class LessonSchema(Schema):
    name = fields.Str(required=True)
    content = fields.Str(required=True)
    lesson_num = fields.Int()
    completed = fields.Bool()

class SectionSchema(Schema):
    name = fields.Str(required=True)
    section_num = fields.Int()
    completed = fields.Bool()
    lessons = fields.Nested(LessonSchema, many=True)
    
class CreateCourseSchema(Schema):
    class Meta:
        unknown = INCLUDE
    name = fields.Str(required=True)
    description = fields.Str()
    hours = fields.Int(required=True)
    num_sections = fields.Int()
    num_enrolled = fields.Int()
    category_id = fields.String()
    instructor_id = fields.String(required=True)

    sections = fields.Nested(SectionSchema, many=True)
    @post_load
    def make_course(self, data, **kwargs):
        # Extract sections data and convert them into Section objects
        sections_data = data.pop('sections', [])
        sections = []

        for section_data in sections_data:
            # Extract lessons data and convert them into Lesson objects
            lessons_data = section_data.pop('lessons', [])
            lessons = [Lesson(**lesson_data) for lesson_data in lessons_data]

            # Create the Section object with the converted lessons and remaining data
            section = Section(lessons=lessons, **section_data)
            sections.append(section)

        # Create the Course object with the converted sections and the remaining data
        return Course(sections=sections, **data)


class UpdateCourseSchema(CourseSchema):
    @post_load
    def update_course(self, data, **kwargs):
        course = self.context.get('instance', None)
        if course:
            for key, value in data.items():
                if key not in ['id', 'created_at', 'updated_at', 'instractor_id']:
                    setattr(course, key, value)
        return course
