import logging
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin

from data_factory import get_data

user_api = Blueprint('user_api', __name__,
                      url_prefix='/user',)


def validate_input_filters(data):
    """
        validate the filter data
    """
    if 'name' not in data or 'date' not in data:
        return False
    return True


@user_api.route('/get_data', methods=['POST'])
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
