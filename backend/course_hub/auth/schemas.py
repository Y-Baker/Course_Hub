from marshmallow import Schema, fields, validates, ValidationError, post_load

from models import storage
from models.user import User


class UserSchema(Schema):
    email = fields.Email(required=True)
    name = fields.String(required=True)
    password = fields.String(required=True)
    age = fields.Integer()

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)

    @validates('email')
    def validate_email(self, value):
        if storage.getUserByEmail(value):
            raise ValidationError("email already exists")

    @validates('name')
    def validate_name(self, value):
        if len(value) < 2:
            raise ValidationError("Name cannot be less than 2 characters")

    @validates('password')
    def validate_password(self, value):
        if len(value) < 6:
            raise ValidationError("Password cannot be less than 6 characters")

    @validates('age')
    def validate_age(self, value):
        if value and value < 9:
            raise ValidationError("Age cannot be less than 9")
