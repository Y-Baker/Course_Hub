#!/usr/bin/python3
"""module init"""
from flask_login import LoginManager, current_user, login_required

from course_hub import app, user_views, auth_views, jwt
from os import getenv
from flask import jsonify
from flask_cors import CORS
from flasgger import Swagger
from models import storage
from course_hub.user import user_views
from course_hub.course import course_views

#registering bluebrints
app.register_blueprint(user_views)
app.register_blueprint(auth_views)
app.register_blueprint(course_views)

#flask_login configurations
login_manager = LoginManager()
login_manager.init_app(app)

#flask_JWT configurations
jwt.init_app(app)

@login_manager.user_loader
def load_user(id):
    print(id)
    return storage.getUserById(id)



@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({'message': 'Unauthorized'}), 401

@app.errorhandler(403)
def unauthorized(err):
    return jsonify({'message': 'not authorized'}), 403

@app.errorhandler(401)
def unauthenticated(err):
    return jsonify({'message': 'not authenticated'}), 401

@app.errorhandler(404)
def not_found(err):
    """handler for 404 errors that returns a JSON-formatted"""
    return jsonify({"error": "Not found"}), 404

Swagger(app)

if __name__ == '__main__':
    host = getenv('CH_API_HOST', '0.0.0.0')
    port = getenv('CH_API_PORT', '5000')
    app.url_map.strict_slashes = False
    app.run(host=host, port=int(port), threaded=True)
