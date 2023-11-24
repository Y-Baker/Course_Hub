#!/usr/bin/python3
"""new view for State objects that handles all default RESTFul API actions"""
from marshmallow import ValidationError

from course_hub.auth import auth_views
from flask import abort, jsonify, request
from models import storage
from models.student import Student
from models.instructor import Instructor
from models.admin import Admin
from flasgger.utils import swag_from
from bcrypt import checkpw
from flask_login import login_user, logout_user, login_required, current_user
from .schemas import UserSchema


@auth_views.route('/sign-up', methods=['POST'])
@swag_from('documentation/auth/sign_up.yml')
def sign_up():
    roles = [Admin, Instructor, Student]
    data = request.get_json()
    try:
        new_user = UserSchema().load(data)
    except ValidationError as e:
        return jsonify({"error": e.messages}), 400
    new_user.save()
    new_data = role_data(data)
    new_data['id'] = new_user.id
    role = roles[new_user.role](**new_data)
    role.save()

    return jsonify({'message': f'user Created Successfully with id {new_user.id}'})


@login_required
@swag_from('documentation/auth/logout.yml')
@auth_views.route('/logout')
def logout():
    """ logout function"""
    if not current_user.is_authenticated:
        abort(401)
    logout_user()
    return jsonify({'message': current_user.name + ' has logged out successfully'})


@auth_views.route('/protected')
@login_required
@swag_from('documentation/auth/protected.yml')
def protected_route():
    return jsonify({'message': 'Access granted for user {}'.format(current_user.email)})


@auth_views.route('/login', methods=['POST'])
@swag_from('documentation/auth/login.yml')
def login():
    if request.method == 'POST':
        data = request.get_json()
        if not data:
            abort(400, "Not a JSON")

        if not data.get('email'):
            abort(400, "Missing email")

        if not data.get('password'):
            abort(400, "Missing password")
        email = data.get('email')
        password = data.get('password')
        remember = data.get('remember')
        if remember:
            try:
                remember = bool(remember)
            except ValueError as ex:
                remember = False
        user = storage.getUserByEmail(email)
        if user:
            userBytes = password.encode('utf-8')
            hashed_password_bytes = user.password.encode('utf-8')
            if checkpw(userBytes, hashed_password_bytes):
                login_user(user, remember=remember)
                return jsonify({'message': 'user logged in successfully'})
        else:
            return jsonify({'message': 'incorrect email or password'})


def notValidInput(email, name, password, age):
    if storage.getUserByEmail(email):
        return "email already exists"
    if name and len(name) < 2:
        return "name cannot be less than 2 characters"
    if len(password) < 6:
        return "password cannot be less than 6 characters"
    if age and age < 9:
        return "age cannot be less than 9"


def role_data(data):
    """update data to handle new role"""
    new_data = {}
    for k, v in data.items():
        if k in ['interested']:
            new_data[k] = v

    return new_data
