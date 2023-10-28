#!/usr/bin/python3
"""handles all default RESTFul API"""

from flask import request, jsonify, abort
from models import User
from api.v1.views import app_views
from models import storage

# Retrieve the list of all User objects
@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])

# Retrieve a User object by user_id
@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())

# Delete a User object by user_id
@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    return jsonify({}), 200

# Create a User
@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if "email" not in data:
        return jsonify({"error": "Missing email"}), 400
    if "password" not in data:
        return jsonify({"error": "Missing password"}), 400

    user = User(**data)
    storage.save_user(user)
    return jsonify(user.to_dict()), 201

# Update a User object by user_id
@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    user = User.get(user_id)
    if not user:
        abort(404)

    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    # Remove keys that should be ignored
    for key in ['id', 'email', 'created_at', 'updated_at']:
        data.pop(key, None)

    user.update(data)
    return jsonify(user.to_dict()), 200
