#!/usr/bin/python3
"""new view for State objects that handles all default RESTFul API actions"""

from course_hub.auth import auth_views
from flask import abort, jsonify, request
from models import storage
from models.user import User
from flasgger.utils import swag_from
from bcrypt import checkpw
from flask_login import login_user, logout_user, login_required, current_user


@auth_views.route('/sign-up', methods=['POST'])
@swag_from('documentation/auth/sign_up.yml')
def sign_up():
    if request.method == 'POST':
        data = request.get_json()
        if not data:
            abort(400, "Not a JSON")

        if not data.get('email'):
            abort(400, "Missing email")

        if not data.get('password'):
            abort(400, "Missing password")
        email = data.get('email')
        name = data.get('name')
        password = data.get('password')
        age = data.get('age')
        if age:
            try:
                age = int(age)
            except ValueError as ex:
                pass
        checked_input = notValidInput(email, name, password, age)
        if checked_input:
            return jsonify({'error': checked_input})
        new_user = User(**{'email': email,
                           'password': password,
                           'name': name,
                           'age': age})
        new_user.save()
        return jsonify({'message': 'user Created Successfully with id' + new_user.id})


@login_required
@swag_from('documentation/auth/logout.yml')
@auth_views.route('/logout')
def logout():
    """ logout function"""
    print(current_user.is_authenticated)
    logout_user()
    return jsonify({'message': 'logged out successfully'})


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
        print(email)
        print(password)
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
