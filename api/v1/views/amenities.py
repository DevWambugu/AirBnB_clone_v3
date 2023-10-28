#!/usr/bin/python3
'''Creates a new view for amenities  objects
that handles all default RESTFul API actions'''

from models.amenity import Amenity
from models.city import City
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/api/v1/amenities',
                 methods=['GET'], strict_slashes=False)
def get_amenities():
    '''Retrieves the list of all amenity objects'''
    amenities_list = []
    all_amenities = storage.all(Amenity).values()

    for amenity in all_amenities:
        all_amenities.append(amenity.to_dict())
    return jsonify(all_amenities)


@app_views.route('/api/v1/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    '''retrieve a amenity object'''
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    '''Deletes a Amenity object'''
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities',
                 methods=['POST'], strict_slashes=False)
def create_amenity():
    '''creates a amenity'''
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    instance = Amenity(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity():
    '''Updates a Amenity object'''
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    to_ignore = ['id', 'created_at', 'updated_at']
    get_data = request.get_json()
    for key, value in get_data.items():
        if key not in to_ignore:
            setattr(amenity, key, value)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
