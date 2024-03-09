import logging

from flask import Blueprint, request, jsonify, send_file
from flask_cors import cross_origin
import boto3

from aws_config import AWS_ACCESS_KEY, AWS_SECRET_KEY, S3_BUCKET


aws_s3_api = Blueprint('aws_s3_api', __name__,
                        url_prefix='/aws_s3',)


# low-level client interface to Amazon S3. It directly maps to the Amazon S3 API
s3_client = boto3.client('s3')

# provides a higher-level, object-oriented API for working with Amazon S3 resources
s3_resource = boto3.resource('s3')


@aws_s3_api.route('/list_buckets', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_bucket_list():
    result = []
    logging.info(f"Getting s3 buckets")
    for bucket in s3_resource.buckets.all():
        result.append(bucket.name)
    return jsonify({"success": True, "message": "successful.",
                        "data": result}), 200


@aws_s3_api.route('/list_objects', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_object_list():
    result = []
    data = request.get_json()
    bucket_name = data.get('bucket_name', S3_BUCKET)
    logging.info(f"Getting s3 bucket objects")

    bucket = s3_resource.Bucket(bucket_name)
    for obj in bucket.objects.all():
        result.appedn(obj.key)

    return jsonify({"success": True, "message": "successful.",
                        "data": result}), 200


@aws_s3_api.route('/add_object', methods=['POST'])
@cross_origin(supports_credentials=True)
def save_s3_object():
    result = []
    data = request.get_json()
    bucket_name = data.get('bucket_name', S3_BUCKET)
    file = request.files['file']
    file_name = file.filename

    logging.info(f"Saving s3 bucket object")

    # s3_key is the file path inside the bucket
    s3_key = f"/{file_name}"

    # if the file is coming in the request as data bytes
    s3_resource.Object(bucket_name, s3_key).put(Body= file.read())

    logging.info(f"Saved the input file {file_name} in the bucket {bucket_name}")

    return jsonify({"success": True, "message": "successful.",
                        "data": result}), 200

@aws_s3_api.route('/delete_object', methods=['POST'])
@cross_origin(supports_credentials=True)
def delete_s3_object():
    result = []
    data = request.get_json()
    bucket_name = data.get('bucket_name', S3_BUCKET)
    file_name = data['file_name']
    logging.info(f"Deleting s3 bucket object")

    # s3_key is the file path inside the bucket
    s3_key = f"/{file_name}"

    s3_resource.Object(bucket_name, s3_key).delete()

    logging.info(f"Deleted the file {file_name} in the bucket {bucket_name}")

    return jsonify({"success": True, "message": "successful.",
                        "data": result}), 200


@aws_s3_api.route('/download_object', methods=['GET'])
@cross_origin(supports_credentials=True)
def download_s3_object():
    result = []
    data = request.get_json()
    bucket_name = data.get('bucket_name', S3_BUCKET)
    file_name = data['file_name']
    logging.info(f"download s3 bucket object")

    # s3_key is the file path inside the bucket
    s3_key = f"/{file_name}"

    obj = s3_resource.Object(bucket_name, s3_key)
    file_stream = obj.get()['Body']

    return send_file(
            file_stream,
            attachment_filename=file_name,
            as_attachment=True
        )
