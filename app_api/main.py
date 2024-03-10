import logging

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, support_credentials=True)

from login import login_api
from user import user_api
from aws_s3 import aws_s3_api
from aws_dynamodb import aws_dynamodb_api

app.register_blueprint(login_api)
app.register_blueprint(user_api)
app.register_blueprint(aws_s3_api)
app.register_blueprint(aws_dynamodb_api)

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

@app.errorhandler(400)
@app.errorhandler(401)
@app.errorhandler(404)
@app.errorhandler(500)
@app.errorhandler(Exception)
def not_found(error):
    error_message = getattr(error, 'description', '')
    error_code = error.code if hasattr(error, 'code') else 500

    if not error_message:
        error_message = str(error)

    return jsonify({"success": False, "message": error_message}), error_code


if __name__ == '__main__':
    app.run(debug=True)
