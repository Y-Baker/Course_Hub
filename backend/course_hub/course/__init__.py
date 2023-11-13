#!/usr/bin/python3
"""initialize the blueprint app (app_views) for FLASK"""

from flask import Blueprint

course_views = Blueprint('app_views', __name__, url_prefix='/api/')
from backend.course_hub.course.views.courses import *
from backend.course_hub.course.views.sections import *
from backend.course_hub.course.views.lessons import *
from backend.course_hub.course.views.index import *
from backend.course_hub.course.views.categories import *
