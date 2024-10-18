"""
Lambda function that receives s3 event trigger, and then copies file from Raw S3 bucket 
into Processing S3 bucket, and deletes it (from Raw bucket) once completed
"""

import json
import logging
import boto3

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize S3 client
s3 = boto3.client('s3')

# Hardcoded target bucket
TARGET_BUCKET = 'snowflake-etlproject-processing'

def lambda_handler(event, context):
    """Lambda function to copy files from the source bucket to the target bucket."""
    
    logger.info("Received event: %s", json.dumps(event))

    results = []
    for record in event['Records']:
        try:
            # Extract bucket and object details
            source_bucket = record['s3']['bucket']['name']
            source_key = record['s3']['object']['key']
            copy_source = {'Bucket': source_bucket, 'Key': source_key}

            logger.info(f"Copying file: {source_key} from {source_bucket} to {TARGET_BUCKET}")

            # Copy the object to the target bucket
            s3.copy_object(CopySource=copy_source, Bucket=TARGET_BUCKET, Key=source_key)

            results.append({'file': source_key, 'status': 'success'})

        except Exception as e:
            logger.error(f"Failed to copy {source_key}: {e}")
            results.append({'file': source_key, 'status': 'failed', 'error': str(e)})

    return {
        'statusCode': 200,
        'body': json.dumps(results)
    }

    
           








