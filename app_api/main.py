import logging

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

from utils import hash_password
from data_factory import get_data


app = Flask(__name__)
CORS(app, support_credentials=True)

# logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

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

def validate_input_filters(data):
    """
        validate the filter data
    """
    if 'name' not in data or 'date' not in data:
        return False
    return True

@app.route('/login', methods=['POST'])
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
    

@app.route('/get_data', methods=['POST'])
@cross_origin(supports_credentials=True)
def get_medical_data():
    logging.info("calling get data method")
    data = request.get_json()

    if not validate_input_filters(data):
        return jsonify({"error": "Both name and date are required."}), 400

    name = data['name']
    date = data['date']

    if (not name) or (not date):
        return jsonify({"success": True, "message": "Enter name and date."}), 400
    try:
        result = get_data(name, date)
        logging.info(f"Result - {result}")

        logging.info("Entered name %s and date %s", name, date)
        return jsonify({"success": True, "message": "successful.",
                        "data": result}), 200
    except Exception as exc:
        logging.error(f"Error occured while retrieving data {str(exc)}")
    

if __name__ == '__main__':
    app.run(debug=True)
