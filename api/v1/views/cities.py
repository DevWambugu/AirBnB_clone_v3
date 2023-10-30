#!/usr/bin/python3
'''Creates a new view for cities  objects
that handles all default RESTFul API actions'''

from models.state import City
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_cities(state_id):
   '''Retrieves the list of all city objects'''
    cities_list = []
    state = storage.get(State, state_id)
    if not state:
        abort(404)
   for city in state.cities:
       cities_list.append(city.to_dict())
   return jsonify(cities_list)


@app_views.route('/cities/<city_id>/', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    '''retrieve a city object'''
     city = storage.get(City, city_id)
    if not city:
       abort(404)
   return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
   '''Deletes a City object'''
   city = storage.get(City, city_id)
    if not city:
       abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities',
                methods=['POST'], strict_slashes=False)
def create_city():
    '''creates a city'''
    if not request.get_json():
       abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

   data = request.get_json()
   instance = City(**data)
   instance.save()
   return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def city_state():
    '''Updates a City object'''
    city = storage.get(City, city_id)
    if not city:
       abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    to_ignore = ['id', 'created_at', 'updated_at']
    get_data = request.get_json()
    for key, value in get_data.items():
        if key not in to_ignore:
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
