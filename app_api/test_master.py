import logging
from flask import Blueprint, request, jsonify, abort
from flask_cors import cross_origin

from aws_config import session
from utils import success_response

test_master_api = Blueprint('test_master_api', __name__,
                            url_prefix='/test',)

# provides a higher-level, object-oriented API for working with Amazon dynamodb resources
dynamodb = session.resource('dynamodb')

TEST_MASTER = "Tests_Information"


@test_master_api.route('/add_tests', methods=['POST'])
@cross_origin(supports_credentials=True)
def add_new_test_items():
    # sample input below
    """
       {
        "items": [
                    {
                        "Name": "ECG",
                    }
                ]
        }
    """
    data = request.get_json()
    # items are rows in dynamodb table
    items = data.get('items')
    logging.info(f"STARTED creating dynamodb table items")

    # Get a reference to the table
    table = dynamodb.Table(TEST_MASTER)

    # Use batch_writer to put items in bulk
    with table.batch_writer() as batch:
        for item in items:
            batch.put_item(Item=item)

    logging.info('Items created successfully')

    return success_response([])


@test_master_api.route('/list_tests', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_all_tests():
    table_name = TEST_MASTER
    logging.info(f"STARTED fetching all tests")

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


@test_master_api.route('/select_test', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_test_items():

    data = request.get_json()
    test_id = data.get('TestID')
    logging.info(f"STARTED fetching a test")

    # Get a reference to the table
    table = dynamodb.Table(TEST_MASTER)

    item_key = {
        'Test_ID': test_id
    }

    # Retrieve the item
    response = table.get_item(Key=item_key)
    item = response.get('Item', {})

    if not item:
        logging.info('Item Not Found')
        abort(404, 'Item Not Found')

    logging.info('Item retrieved successfully')

    return success_response(item)


@test_master_api.route('/update_test', methods=['POST'])
@cross_origin(supports_credentials=True)
def update_test():
    data = request.get_json()
    test_id = data.get('Test_ID')
    updated_name = data.get('updated_name')

    logging.info(f"STARTED fetching a test")

    # Get a reference to the table
    table = dynamodb.Table(TEST_MASTER)

    item_key = {
        'Test_ID': test_id
    }

    # Specify the attributes to update
    update_expression = "SET #name = :name_value"
    expression_attribute_names = {
        '#name': 'Test_Name',
    }
    expression_attribute_values = {
        ':name_value': updated_name
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


@test_master_api.route('/delete_test', methods=['POST'])
@cross_origin(supports_credentials=True)
def delete_test():
    data = request.get_json()
    test_id = data.get('Test_ID')

    logging.info("STARTED deleting a Test")

    # Get a reference to the table
    table = dynamodb.Table(TEST_MASTER)

    item_key = {
        'Test_ID': test_id
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
