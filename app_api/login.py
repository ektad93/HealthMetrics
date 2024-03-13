import logging
from flask import Blueprint, request, abort
from flask_cors import cross_origin

from utils import hash_password, success_response

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
        return abort(400, "Both username and password are required.")

    username = data['username']
    password = data['password']

    if (not username) or (not password):
        return abort(400, "Enter username and password")

    if username in USER_DETAILS and USER_DETAILS[username] == hash_password(password):
        logging.info("Successful login for the user --> %s", username)
        return success_response("Login successful. We will provide a token in future")
    else:
        return abort(401, "Invalid username or password")
