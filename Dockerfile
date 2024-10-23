# Use the official AWS Lambda Python 3.9 image as the base
FROM public.ecr.aws/lambda/python:3.9

# Copy the Lambda function code into the container
COPY lambda_function.py ${LAMBDA_TASK_ROOT}/

# Install boto3 (in case it's not already included in the base image)
RUN pip install boto3

# Set the handler to lambda_function.lambda_handler
CMD ["lambda_function.lambda_handler"]

