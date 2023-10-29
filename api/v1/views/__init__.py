#!/usr/bin/python3
'''import blueprint'''
from flask import Blueprint
from models import storage

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
app = Flask(__name__)
app.register_blueprint(app_views)


from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *

if __name__ == '__main__':
    app.run(host=host, port=port)
