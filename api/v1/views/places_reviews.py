#!/usr/bin/python3
"""creates a new view for review object that handles
    all default RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User

@app_views.route('/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)

@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())

@app_views.route('/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200

@app_views.route('/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    user_id = data.get("user_id")
    if user_id is None:
        return jsonify({"error": "Missing user_id"}), 400

    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    text = data.get("text")
    if text is None:
        return jsonify({"error": "Missing text"}), 400

    new_review = Review(**data)
    new_review.place_id = place_id
    new_review.save()

    return jsonify(new_review.to_dict()), 201

@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    # Ignore keys: id, user_id, place_id, created_at, and updated_at
    keys_to_ignore = ["id", "user_id", "place_id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in keys_to_ignore:
            setattr(review, key, value)
    review.save()

    return jsonify(review.to_dict()), 200
