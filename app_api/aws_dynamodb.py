import logging
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin

aws_dynamodb_api = Blueprint('aws_dynamodb_api', __name__,
                              url_prefix='/aws_dynamodb')
