#!/usr/bin/python3
""" validation for class Section"""

from marshmallow import Schema, fields, INCLUDE, post_load
from marshmallow import validate, validates, ValidationError

from models import storage
from models.section import Section
from models.course import Course


class SectionSchema(Schema):
    class Meta:
        unknown = INCLUDE
    name = fields.String(required=True)
    section_num = fields.Integer(validate=validate.Range(min=1))
    course_id = fields.String(required=True)

    @validates('name')
    def validate_name(self, value):
        if len(value) < 3:
            raise ValidationError("Name cannot be less than 3 characters")

    @validates('course_id')
    def validate_course_id(self, value):
        if not storage.get(Course, value):
            raise ValidationError("Course doesn't exist")

    @validates('section_num')
    def validate_section_num(self, value):
        course_id = self.context.get('data', {}).get('course_id')
        course = storage.get(Course, course_id)
        section = self.context.get('instance', None)
        if course:
            list_sections = course.sections
            if section:
                list_sections = [one for one in list_sections
                                if one.id != section.id]

            section_nums = [section.section_num for section in course.sections]

            if value in section_nums:
                raise ValidationError("section_num already exists")


class CreateSectionSchema(SectionSchema):
    @post_load
    def make_Section(self, data, **kwargs):
        return Section(**data)


class UpdateSectionSchema(SectionSchema):
    @post_load
    def update_Section(self, data, **kwargs):
        section = self.context.get('instance', None)
        if section:
            for key, value in data.items():
                if key not in ['id', 'created_at', 'updated_at', 'course_id']:
                    setattr(section, key, value)
        return section
