from __future__ import print_function
import boto3
import json

message_queue = boto3.client('sqs',region_name="us-east-1")
amazon_ses =    boto3.client('ses',region_name="us-east-1")
# set these at environment variables
QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/785975698029/testing-SES.fifo'
#email of the sender
SENDER = "Saqib Mehraj <saqib.mehraj@comprinno.net>"
#recipient email verified in SES 
RECIPIENT = "saqibmehraj2@gmail.com"    
CHARSET = 'UTF-8'

def lambda_handler(event, context):
    for record in event['Records']:
        payload = str(record["body"])
        #print(str(payload))

    response = message_queue.receive_message(
        QueueUrl=QUEUE_URL,
        AttributeNames=[
            'SentTimestamp'
        ],
        MaxNumberOfMessages=10,
        MessageAttributeNames=[
            'All'
        ],
        VisibilityTimeout=1,
        WaitTimeSeconds=0
    )
    response = amazon_ses.send_email(
        Source=SENDER,
        Destination={
            'ToAddresses': [
                    RECIPIENT,
            ],
        },
        Message={
            'Subject': {
                'Data': 'This is a test email',
                'Charset': CHARSET
            },
            'Body': {
                'Text': {
                    'Data': payload,
                    'Charset': CHARSET
                }
            }
        }
    )

    return 'EMAIL SENT'
