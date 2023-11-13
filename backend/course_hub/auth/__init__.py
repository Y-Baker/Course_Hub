#!/usr/bin/python3
"""initialize the blueprint app (app_views) for FLASK"""

from flask import Blueprint

auth_views = Blueprint('auth_views', __name__, url_prefix='/api/')
from course_hub.auth.views import *
