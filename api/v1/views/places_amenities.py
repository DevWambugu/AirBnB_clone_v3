#!/usr/bin/python3
"""Creates a new view for the link between Place objects
    and Amenity objects that handles all default REASTFul
    Api actions"""

from flask import Flask, request, abort, jsonify
from models import storage
from models.place import Place
from models.amenity import Amenity
from api.v1.views import app_views

@app_views.route('/places/<place_id>/amenities', methods=['GET'], strict_slashes=False)
def get_amenities(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    amenities = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(amenities)

@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity_from_place(place_id, amenity_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if amenity not in place.amenities:
        abort(404)

    place.amenities.remove(amenity)
    storage.save()
    return jsonify({}), 200

@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'], strict_slashes=False)
def link_amenity_to_place(place_id, amenity_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200

    place.amenities.append(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201
