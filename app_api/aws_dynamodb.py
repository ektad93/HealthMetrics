import logging
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin

from aws_config import session
from utils import success_response

aws_dynamodb_api = Blueprint('aws_dynamodb_api', __name__,
                              url_prefix='/aws_dynamodb')


# provides a higher-level, object-oriented API for working with Amazon dynamodb resources
dynamodb = session.resource('dynamodb')


@aws_dynamodb_api.route('/list_tables', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_all_tables():
    logging.info(f"Getting dynamodb tables")
    tables = list(dynamodb.tables.all())
    return success_response(tables)



@aws_dynamodb_api.route('/delete_table', methods=['POST'])
@cross_origin(supports_credentials=True)
def delete_dynamodb_table():
    data = request.get_json()
    table_name = data.get('table_name')
    logging.info(f"STARTED deleting dynamodb table {table_name}")

    # Get a reference to the table
    table = dynamodb.Table(table_name)

    # Delete the table
    table.delete()

    # Wait for the table to be deleted
    table.meta.client.get_waiter('table_not_exists').wait(TableName=table_name)

    logging.info(f"Successfully deleted table {table_name}")

    return success_response([])