#!/usr/bin/python3
""" Creates a new view for place objects
    that handles all default RESTFul API actions"""

from flask import Flask, request, abort, jsonify
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User

@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_places_in_city(city_id):
    city = City.query.get(city_id)
    if not city:
        abort(404)

    places = [place.to_dict() for place in Place.query.filter_by(city_id=city_id)
    return jsonify(places)

@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    place = Place.query.get(place_id)
    if not place:
        abort(404)

    return jsonify(place.to_dict())

@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    place = Place.get(place_id)
    if not place:
        abort(404)

    place.delete()
    return jsonify({}), 200

@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    city = City.get(city_id)
    if not city:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if "user_id" not in data:
        abort(400, "Missing user_id")

    user = User.get(data["user_id"])
    if not user:
        abort(404)

    if "name" not in data:
        abort(400, "Missing name")

    place = Place(**data)
    place.city_id = city_id
    place.save()

    return jsonify(place.to_dict()), 201

@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    place = Place.get(place_id)
    if not place:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    ignore_keys = ["id", "user_id", "city_id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)

    place.save()

    return jsonify(place.to_dict()), 200
