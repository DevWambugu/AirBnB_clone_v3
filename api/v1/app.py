#!/usr/bin/python3
'''create a variable app, instance of Flask'''

from models import storage
from api.v1.views import app_views
from flask import Flask
from flask_cors import CORS
from os import environ
from flask import jsonify
from flask import make_response
from flask import render_template

app = Flask(__name__)
#CORS(app)
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(error):
    '''returns a 404 error'''
    return make_response(jsonify({'error': "Not found"}), 404)


@app.teardown_appcontext
def close_db(error):
    '''calls storage.close'''
    storage.close()


if __name__ == "__main__":
    '''run the app'''
    host = environ.get('HBNB_API_HOST')
    port = environ.get('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
