import logging
from flask import Blueprint, request, jsonify, abort
from flask_cors import cross_origin

from aws_config import session
from utils import success_response

user_api = Blueprint('user_api', __name__,
                      url_prefix='/user',)

# provides a higher-level, object-oriented API for working with Amazon dynamodb resources
dynamodb = session.resource('dynamodb')

USER_TABLE = "usersTable"

@user_api.route('/add_users', methods=['POST'])
@cross_origin(supports_credentials=True)
def add_user_items():
    # sample input below
    """
       {
        "items": [
                    {
                        "Email": "test@alphagenesislabs.com",
                        "First_Name": "test",
                        "Last_Name": "TestLast",
                        "Password": "",
                        "Profile_pic": "",
                        "User_ID": "3"
                    }
                ]
        }
    """
    data = request.get_json()
    # items are rows in dynamodb table
    items = data.get('items')
    logging.info(f"STARTED creating dynamodb table items")

    # Get a reference to the table
    table = dynamodb.Table(USER_TABLE)

    # Use batch_writer to put items in bulk
    with table.batch_writer() as batch:
        for item in items:
            batch.put_item(Item=item)

    logging.info('Items created successfully')

    return success_response([])


@user_api.route('/list_users', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_all_users():
    table_name = USER_TABLE
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
    user_id = data.get('User_ID')
    logging.info(f"STARTED fetching a user")

    # Get a reference to the table
    table = dynamodb.Table(USER_TABLE)

    item_key = {
        'User_ID': user_id
    }

    # Retrieve the item
    response = table.get_item(Key=item_key)
    item = response.get('Item', {})

    if not item:
        logging.info('Item Not Found')
        abort(404, 'Item Not Found')

    logging.info('Item retrieved successfully')

    return success_response(item)


@user_api.route('/update_user', methods=['POST'])
@cross_origin(supports_credentials=True)
def update_user():
    data = request.get_json()
    user_id = data.get('User_ID')
    updated_name = data.get('updated_name')
    updated_email = data.get('updated_email')

    logging.info(f"STARTED fetching a user")

    # Get a reference to the table
    table = dynamodb.Table(USER_TABLE)

    item_key = {
        'User_ID': user_id
    }

    # Specify the attributes to update
    update_expression = "SET #name = :name_value, #email = :email_value"
    expression_attribute_names = {
        '#name': 'First_Name',
        '#email': 'Email'
    }
    expression_attribute_values = {
        ':name_value': updated_name,
        ':email_value': updated_email
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


@user_api.route('/delete_user', methods=['POST'])
@cross_origin(supports_credentials=True)
def delete_user():
    data = request.get_json()
    user_id = data.get('User_ID')

    logging.info("STARTED deleting a user")

    # Get a reference to the table
    table = dynamodb.Table(USER_TABLE)

    item_key = {
        'User_ID': user_id
    }

    # Delete the item
    response = table.delete_item(
        Key=item_key,
        ReturnValues="ALL_OLD"  # Specify to return the deleted item
    )

    # Retrieve the deleted item
    deleted_item = response.get('Attributes', None)

    if not deleted_item:
        logging.info('Item Not found or deleted')
        abort(404, 'Item Not found or deleted')

    logging.info('Item deleted successfully')

    return success_response(deleted_item)
