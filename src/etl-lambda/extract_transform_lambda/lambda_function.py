import json
import urllib.parse
import boto3
import csv
from io import StringIO
from TJClean import parse_csv


def lambda_handler(event, context):
    # Extract bucket and key from the S3 event
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')


    print(f'source bucket: {source_bucket}')
    print(f'key: {key}')

    # Retrieve S3 object content
    s3_resource = boto3.resource('s3')
    s3 = boto3.client('s3')
    # s3_object = s3_resource.Object(source_bucket, key)
    # data = s3_object.get()['Body'].read().decode('utf-8').splitlines()
    file_obj = s3.get_object(Bucket=source_bucket, Key=key)
    file_content = file_obj['Body'].read().decode('utf-8')
    # print(data)
    
    parsed_data = parse_csv(file_content)
    
            
     # Convert the modified data back to CSV
    csv_buffer = StringIO()
    headers = ['SCRAPE_DATE', 'SKILLS', 'SALARY', 'HREF', 'TITLE', 'JOB_DESC', 'POSTDATE', 'RECRUITER']  # Replace with your actual field names
    csv_writer = csv.DictWriter(csv_buffer, fieldnames=headers)
    csv_writer.writeheader()
    csv_writer.writerows(parsed_data)
    modified_file_content = csv_buffer.getvalue()
    
    # Write the modified file to the new bucket
    destination_bucket = 'cleandata-snowflake'
    s3.put_object(Body=modified_file_content, Bucket=destination_bucket, Key=key)