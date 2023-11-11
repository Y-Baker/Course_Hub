#!/usr/bin/python
"""module init"""


from flask import Flask
app = Flask(__name__)

app.config.from_object('config.default')


app.config.from_envvar('APP_CONFIG_FILE')
