#!/usr/bin/python3
"""new view for State objects that handles all default RESTFul API actions"""
from marshmallow import ValidationError

import os
from course_hub.auth import auth_views
from flask import abort, jsonify, request
from models import storage
from models.TokenBlocklist import TokenBlocklist
from models.student import Student
from models.instructor import Instructor
from models.admin import Admin
from flasgger.utils import swag_from
from bcrypt import checkpw
from flask_login import login_user, logout_user, login_required, current_user as loggedIn_user
from .schemas import SignUpSchema, SignInSchema
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt,
    current_user,
    get_jwt_identity,
)

current_directory = os.path.dirname(os.path.realpath(__file__))

@auth_views.route('/sign-up', methods=['POST'])
@swag_from(os.path.join(current_directory, 'documentation/auth/sign_up.yml'))
def sign_up():
    roles = [Admin, Instructor, Student]
    data = request.get_json()
    try:
        new_user = SignUpSchema().load(data)
    except ValidationError as e:
        return jsonify({"error": e.messages}), 400
    new_user.save()
    new_data = role_data(data)
    new_data['id'] = new_user.id
    role = roles[new_user.role](**new_data)
    role.save()

    return jsonify({'message': f'user Created Successfully with id {new_user.id}'})


# @login_required
# @swag_from('documentation/auth/logout.yml')
# @swag_from(os.path.join(current_directory, 'documentation/auth/logout.yml'))
# @auth_views.route('/logout')
# def logout():
#     """ logout function"""
#     if not current_user.is_authenticated:
#         abort(401)
#     logout_user()
#     return jsonify({'message': current_user.name + ' has logged out successfully'})


@auth_views.get("/refresh")
@jwt_required(refresh=True)
def refresh_access():
    additional_claims = {"role": current_user.role, "email": current_user.email}
    new_access_token = create_access_token(identity=current_user.id, additional_claims=additional_claims)

    return jsonify({"access_token": new_access_token})


@auth_views.get('/logout')
@login_required
# @swag_from('documentation/auth/logout.yml')
@swag_from(os.path.join(current_directory, 'documentation/auth/logout.yml'))

@jwt_required(verify_type=False) 
def logout_user():
    jwt = get_jwt()

    jti = jwt.get('jti')
    token_type = jwt.get('type')

    token_b = TokenBlocklist(jti=jti)
    token_b.save()
    logout_user()
    return jsonify({"message": f"{token_type} token revoked successfully"}) , 200

@auth_views.route('/protected')
@jwt_required()
@login_required
# @swag_from('documentation/auth/protected.yml')
@swag_from(os.path.join(current_directory, 'documentation/auth/protected.yml'))

def protected_route():
    return jsonify({'message': 'Access granted for user {}'.format(current_user.email)})


@auth_views.route('/login', methods=['POST'])
# @swag_from('documentation/auth/login.yml')
@swag_from(os.path.join(current_directory, 'documentation/auth/login.yml'))

def login():
    data = SignInSchema().load(data=request.get_json())
    email = data.get('email')
    password = data.get('password')
    remember = data.get('remember')
    user = storage.getUserByEmail(email)
    if user:
        userBytes = password.encode('utf-8')
        hashed_password_bytes = user.password.encode('utf-8')
        if checkpw(userBytes, hashed_password_bytes):
            additional_claims = {"role": user.role, "email": user.email}
            access_token = create_access_token(identity=user.id, additional_claims=additional_claims)
            refresh_token = create_refresh_token(identity=user.id, additional_claims=additional_claims)
            login_user(user, remember=remember)
            return jsonify({
                'message': 'user logged in successfully',
                'tokens' : {
                    "access_token" : access_token, 
                    "refresh_token" : refresh_token
                }
            }), 200
    else:
        return jsonify({'message': 'incorrect email or password'})
    
@auth_views.get("/whoami")
@jwt_required()
def whoami():
    return jsonify(
        {
            "message": "message",
            "user_details": {
                "name": current_user.name,
                "email": current_user.email,
            },
        }
    )


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
