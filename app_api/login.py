import logging
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin

from utils import hash_password

login_api = Blueprint('login_api', __name__,
                       url_prefix='/login',)


# usernames and encoded passwords
USER_DETAILS = {
    "user": "$2b$12$rHcOz3tq9kNxwLBC2dmBCer3IyoZx7WaRl.HSwUSKV7EBrDRycf.q"
}


def validate_login_data(data):
    """
        validate the input login form data
    """
    if 'username' not in data or 'password' not in data:
        return False
    return True


@login_api.route('', methods=['POST'])
@cross_origin(supports_credentials=True)
def login():
    data = request.get_json()
    if not validate_login_data(data):
        return jsonify({"error": "Both username and password are required."}), 400

    username = data['username']
    password = data['password']

    if (not username) or (not password):
        return jsonify({"success": True, "message": "Enter username and password."}), 400

    if username in USER_DETAILS and USER_DETAILS[username] == hash_password(password):
        logging.info("Successful login for the user --> %s", username)
        return jsonify({"success": True, "message": "Login successful."}), 200
    else:
        return jsonify({"success": False, "message": "Invalid username or password."}), 401

