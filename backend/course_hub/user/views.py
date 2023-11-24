#!/usr/bin/python3
"""new view for State objects that handles all default RESTFul API actions"""

from course_hub.user import user_views
from flask import jsonify, abort, request
from models import storage
from models.user import User
from flasgger.utils import swag_from
from bcrypt import checkpw
from flask_login import login_user, logout_user, login_required, current_user


@user_views.route('/users', methods=['GET'])
@swag_from('documentation/user/all_users.yml')
def get_users():
    """reterive all users from storage
    """
    return jsonify(list(map(lambda user:
                            user.to_dict(), storage.all(User).values())))


@user_views.route('/users/<user_id>', methods=['GET'])
@swag_from('documentation/user/get_user.yml', methods=['GET'])
def get_user(user_id):
    """reterive user by id
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@user_views.route('/users/<user_id>', methods=['DELETE'])
@swag_from('documentation/user/delete_user.yml', methods=['DELETE'])
def delete_users(user_id):
    """delete user by id
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({}), 200



@user_views.route('/users/<user_id>', methods=['PUT'])
@swag_from('documentation/user/put_user.yml', methods=['PUT'])
def update_user(user_id):
    """update user to storage
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')

    for k, v in data.items():
        if k not in ['id', 'created_at', 'updated_at', 'email']:
            setattr(user, k, v)

    user.save()
    return jsonify(user.to_dict())
