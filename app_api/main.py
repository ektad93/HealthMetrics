import logging

from flask import Flask
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


if __name__ == '__main__':
    app.run(debug=True)
