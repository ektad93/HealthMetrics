import logging
from flask import Blueprint, request, jsonify, abort
from flask_cors import cross_origin

from aws_config import session
from utils import success_response

user_api = Blueprint('user_api', __name__,
                      url_prefix='/user',)

# provides a higher-level, object-oriented API for working with Amazon dynamodb resources
dynamodb = session.resource('dynamodb')

def validate_input_filters(data):
    """
        validate the filter data
    """
    if 'name' not in data or 'date' not in data:
        return False
    return True

@user_api.route('/add_users', methods=['POST'])
@cross_origin(supports_credentials=True)
def add_user_items():
    """
        sample input
        {
            "table_name": "Users",
            "items": [{
                    'id': 1,
                    'name': 'John',
                    'age': 25,
                    'email': 'john.doe@gmail.com'
                }]
        }
    """
    data = request.get_json()
    table_name = data.get('table_name')
    # items are rows in dynamodb table
    items = data.get('items')
    logging.info(f"STARTED creating dynamodb table items")

    # Get a reference to the table
    table = dynamodb.Table(table_name)

    # Use batch_writer to put items in bulk
    with table.batch_writer() as batch:
        for item in items:
            batch.put_item(Item=item)

    logging.info('Items created successfully')

    return success_response([])


@user_api.route('/list_users', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_all_users():
    data = request.get_json()
    table_name = data.get('table_name')

    logging.info(f"STARTED fetching all users")

    # Get a reference to the table
    table = dynamodb.Table(table_name)

    result = []
    response = table.scan()
    result = response.get('Items', [])
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        result.extend(response.get('Items', []))

    logging.info('Items retrieved successfully')

    return success_response(result)


@user_api.route('/select_user', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_user_items():
    data = request.get_json()
    table_name = data.get('table_name')

    logging.info(f"STARTED fetching a user")

    # Get a reference to the table
    table = dynamodb.Table(table_name)

    item_key = {
        'UserId': 1
    }

    # Retrieve the item
    response = table.get_item(Key=item_key)
    item = response.get('Item', {})

    if not item:
        logging.info('Item Not Found')
        abort(404, 'Item Not Found')

    logging.info('Item retrieved successfully')

    return success_response(item)



@user_api.route('/update_user', methods=['GET'])
@cross_origin(supports_credentials=True)
def update_user():
    data = request.get_json()
    table_name = data.get('table_name')

    logging.info(f"STARTED fetching a user")

    # Get a reference to the table
    table = dynamodb.Table(table_name)

    item_key = {
        'UserId': 1
    }

    # Specify the attributes to update
    update_expression = "SET #name = :name_value, #email = :email_value"
    expression_attribute_names = {
        '#name': 'name',
        '#email': 'email'
    }
    expression_attribute_values = {
        ':name_value': 'Jane',  # Updated name
        ':email_value': 'jane.doe@example.com'  # Updated email
    }

    # Update the item
    response = table.update_item(
        Key=item_key,
        UpdateExpression=update_expression,
        ExpressionAttributeNames=expression_attribute_names,
        ExpressionAttributeValues=expression_attribute_values,
        ReturnValues="ALL_NEW"  # Specify to return the updated item
    )

    # Retrieve the item
    updated_item = response.get('Attributes', None)

    if not updated_item:
        logging.info('Item Not updated')
        abort(500, 'Item Not updated')

    logging.info('Item updated successfully')

    return success_response(updated_item)
