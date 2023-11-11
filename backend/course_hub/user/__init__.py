#!/usr/bin/python3
"""initialize the blueprint app (app_views) for FLASK"""

from flask import Blueprint

user_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
from course_hub.user.views import *
