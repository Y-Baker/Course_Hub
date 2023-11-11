#!/usr/bin/python
"""module init"""


from course_hub import app
from os import getenv
from flask import jsonify, url_for
from flask_cors import CORS
from flasgger import Swagger
from course_hub.user import user_views


app.register_blueprint(user_views)


@app.errorhandler(404)
def not_found(err):
    """handler for 404 errors that returns a JSON-formatted"""
    return jsonify({"error": "Not found"}), 404

app.config['SWAGGER'] = {
    'title': 'course hub Restful API',
    'uiversion': 3
}

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()

    return len(defaults) >= len(arguments)



@app.route("/site-map")
def site_map_route():
    routes = []

    for rule in app.url_map.iter_rules():
        # Exclude rules that require parameters and rules you can't open in a browser
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            routes.append((url, rule.endpoint))
    return routes

Swagger(app)

if __name__ == '__main__':
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', '5000')
    app.url_map.strict_slashes = False
    app.run(host=host, port=int(port), threaded=True)
