#!/usr/bin/python3
'''returns a json file'''

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    '''defines the status of the api'''
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def number_of_objects():
    '''retrieves the number of each objects by type'''
    classes = [Amenity, City, Place, Review, State, User]
    names = ["amenities", "cities", "places", "reviews", "states", "users"]
    number_of_objs = {}
    for i in range(len(classes)):
        number_of_objs[names[i]] = storage.count(classes[i])
    return jsonify(number_of_objs)
