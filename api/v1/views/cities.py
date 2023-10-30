#!/usr/bin/python3
 '''Creates a new view for cities  objects
that handles all default RESTFul API actions'''

from models.city import City
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    '''Retrieves the list of all city objects for a given state'''
    state = storage.get(State, state_id)
    if not state:
        return jsonify({"error": "Not found"}), 404
    cities_list = [city.to_dict() for city in state.cities]
    return jsonify(cities_list)

@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    '''Retrieve a city object by its ID'''
    city = storage.get(City, city_id)
    if not city:
        return jsonify({"error": "Not found"}), 404
    return jsonify(city.to_dict())

# For the delete route, you can use a try-except block to catch exceptions.
@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    '''Deletes a City object by its ID'''
    city = storage.get(City, city_id)
    if not city:
        return jsonify({"error": "Not found"}), 404
    try:
        storage.delete(city)
        storage.save()
    except Exception:
        return jsonify({"error": "Internal Server Error"}), 500
    return jsonify({})

# For the create route, make sure to set the state_id in the new city object.
@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    '''Creates a city associated with a state'''
    state = storage.get(State, state_id)
    if not state:
        return jsonify({"error": "Not found"}), 404

    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400

    data = request.get_json()
    data['state_id'] = state_id
    instance = City(**data)
    instance.save()
    return jsonify(instance.to_dict()), 201

@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    '''Updates a City object by its ID'''
    city = storage.get(City, city_id)
    if not city:
        return jsonify({"error": "Not found"}), 404

    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400

    to_ignore = ['id', 'state_id', 'created_at', 'updated_at']
    get_data = request.get_json()
    for key, value in get_data.items():
        if key not in to_ignore:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
