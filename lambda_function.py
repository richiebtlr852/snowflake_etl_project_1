"""
Lambda function that receives an S3 event trigger, copies a file from the Raw S3 bucket 
to the 'snowpipe' folder within the target bucket, and deletes it from the source bucket.
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
    """Lambda function to copy files from the source bucket to the 'snowpipe' folder in the target bucket."""
    
    logger.info("Received event: %s", json.dumps(event))

    results = []
    for record in event['Records']:
        try:
            # Extract bucket and object details
            source_bucket = record['s3']['bucket']['name']
            source_key = record['s3']['object']['key']
            copy_source = {'Bucket': source_bucket, 'Key': source_key}

            # Define the new key with the 'snowpipe/' prefix
            target_key = f"snowpipe/{source_key.split('/')[-1]}"  # Ensures only filename is used
            
            logger.info(f"Copying file: {source_key} from {source_bucket} to {TARGET_BUCKET}/{target_key}")

            # Copy the object to the target bucket under 'snowpipe/' folder
            s3.copy_object(CopySource=copy_source, Bucket=TARGET_BUCKET, Key=target_key)

            # Delete the object from the source bucket
            s3.delete_object(Bucket=source_bucket, Key=source_key)
            logger.info(f"Deleted file: {source_key} from {source_bucket}")

            results.append({'file': source_key, 'status': 'success', 'target_key': target_key})

        except Exception as e:
            logger.error(f"Failed to copy {source_key}: {e}")
            results.append({'file': source_key, 'status': 'failed', 'error': str(e)})

    return {
        'statusCode': 200,
        'body': json.dumps(results)
    }

           








