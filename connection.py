import boto3
import logging
import os
import botocore

logging.basicConfig(filename = 'connec_log',level=logging.INFO)

def bucket_lists():
    """
    Read the existing list of buckets in the AWS account.
    """
    try:
        s3 = boto3.resource('s3')
        buckets = list(s3.buckets.all())
        if buckets:
            logging.info("Buckets exist:")
            for bucket in buckets:
                logging.info(bucket.name)
        else:
            logging.info("No buckets found.")
    except boto3.exceptions.Boto3Error as e:
        logging.error(e)
        return False
    return True

def create_bucket(bucket_name, region=None):
    """
    Create new S3 bucket with the given name and region will optional.
    """
    try:
        s3 = boto3.resource('s3')
        create_kwargs = {'Bucket': bucket_name}
        if region is not None:
            create_kwargs['CreateBucketConfiguration'] = {'LocationConstraint': region}
        s3.create_bucket(**create_kwargs)
    except boto3.exceptions.Boto3Error as e:
        if isinstance(e, botocore.exceptions.ClientError) and e.response['Error']['Code'] == 'BucketAlreadyExists':
            logging.error(f"Bucket '{bucket_name}' already exists. Choose a different bucket name.")
        else:
            logging.error(e)
        return False
    return True

def upload_file(file_name, bucket_name, object_name=None):
    """
    Uploading  file to the specified S3 bucket.
    """
    s3 = boto3.resource('s3')
    try:
        # Check if the bucket exists
        if not s3.Bucket(bucket_name) in s3.buckets.all():
            # Create the bucket if it doesn't exist
            create_bucket(bucket_name)
        
        bucket = s3.Bucket(bucket_name)
        if object_name is None:
            object_name = os.path.basename(file_name)
        bucket.upload_file(file_name, object_name)
    except boto3.exceptions.Boto3Error as e:
        logging.error(e)
        return False
    return True

bucket_lists()
create_bucket('rohitsteel','ap-south-1')
upload_file('output.csv', 'rohitsteel')


