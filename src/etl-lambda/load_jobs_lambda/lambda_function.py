import os
import snowflake
import snowflake.connector

import csv
from io import StringIO
import boto3
import uuid

import ast
from urllib.parse import unquote
import re

# Environment variables for Snowflake credentials and connection details
SNOWFLAKE_ACCOUNT = 'EJ50554'
SNOWFLAKE_URL = 'vf32796.eu-west-2.aws'
SNOWFLAKE_USER = 'rupertf'
SNOWFLAKE_PASSWORD = 'Rillyrally42'
SNOWFLAKE_WAREHOUSE = 'COMPUTE_WH'
SNOWFLAKE_DATABASE = 'SKILLNET_DATABASE'
SNOWFLAKE_SCHEMA = 'SKILLNET_SCHEMA'
# Assume the S3 bucket and file path can be derived from the Lambda event
# and that your AWS credentials for Snowflake are configured for S3 access


def load_totalJobs(jobs, cs):
    for job in jobs:
        # Create a JOB ID
        job['job_id'] = str(uuid.uuid4())
        
        # Access the 'skills' column and convert it from string to list
        skills_str = job['SKILLS']
        skills_list = ast.literal_eval(skills_str)
        
        salary = job['SALARY']
        try:
            salary_list = ast.literal_eval(salary)
            if len(salary_list) == 0:
                salary = 30000
            elif len(salary_list) == 1:
                salary = salary_list[0]
            else:
                salary = (salary_list[0] + salary_list[1]) / 2
            
        except:
            # print(type(salary))
            salary = 30000
        
        job['SALARY'] = salary    
        
        insert_sql = """INSERT INTO Jobs (job_id, job_title, Date_posted, Salary, Job_poster, recruiter) VALUES (%s, %s, %s, %s, %s, %s)"""
        cs.execute(insert_sql, (job['job_id'], job['TITLE'], job['SCRAPE_DATE'], job['SALARY'], 'Total Jobs', job['RECRUITER']))
        
        skills = []
        
        for skill in skills_list:
            check_sql = """SELECT Skill_id FROM Skills WHERE Skill_name = %s"""
            cs.execute(check_sql, skill)
            existing_skill_id = cs.fetchone()
            
            if existing_skill_id is None:
                skill_id = str(uuid.uuid4())
                
                insert_sql = """INSERT INTO Skills (Skill_id, Skill_name) VALUES (%s, %s)"""
                cs.execute(insert_sql, (skill_id, skill))
                
                skills.append(skill_id)
            else:
                skill_id = existing_skill_id
                skills.append(existing_skill_id)
                
        skills_list = skills
        
        for skill_id in skills:
            insert_sql = """INSERT INTO Job_Skills (Skill_id, Job_id) VALUES (%s, %s)"""
            cs.execute(insert_sql, (skill_id, job['job_id']))
            

def extract_salary(salary_string):
    if "Competitive Salary - Negotiable" in salary_string:
        return 35000  # Assuming 35000 as a default value for "Competitive Salary - Negotiable"
    elif "£" in salary_string:
        # Extracting numerical values using regular expressions
        numbers = re.findall(r'\d{2,3},?\d{3}', salary_string)
        if len(numbers) == 2:
            # If there are two values, calculate the average
            avg_salary = sum(int(num.replace(',', '')) for num in numbers) / 2
            return avg_salary
        elif numbers:
            # If there's only one value, return that value
            return int(numbers[0].replace(',', ''))
    return 35000  # Return None if no valid salary information is found


def load_indeed_jobs(jobs, cs):
    for job in jobs:
        # Create a JOB ID
        job['job_id'] = str(uuid.uuid4())
        
        # Access the 'skills' column and convert it from string to list
        skills_str = job['skills']
        skills_list = ast.literal_eval(skills_str)
        
        salary = extract_salary(job['salary'])
        
        insert_sql = """INSERT INTO Jobs (job_id, job_title, Date_posted, Salary, Job_poster, recruiter) VALUES (%s, %s, %s, %s, %s, %s)"""
        cs.execute(insert_sql, (job['job_id'], job['job_title'], job['date_posted'], salary, 'Indeed', job['company_name']))

        skills = []
        
        for skill in skills_list:
            check_sql = """SELECT Skill_id FROM Skills WHERE Skill_name = %s"""
            cs.execute(check_sql, skill)
            existing_skill_id = cs.fetchone()
            
            if existing_skill_id is None:
                skill_id = str(uuid.uuid4())
                
                insert_sql = """INSERT INTO Skills (Skill_id, Skill_name) VALUES (%s, %s)"""
                cs.execute(insert_sql, (skill_id, skill))
                
                skills.append(skill_id)
            else:
                skill_id = existing_skill_id
                skills.append(existing_skill_id)
                
        skills_list = skills
        
        for skill_id in skills:
            insert_sql = """INSERT INTO Job_Skills (Skill_id, Job_id) VALUES (%s, %s)"""
            cs.execute(insert_sql, (skill_id, job['job_id']))
            

def lambda_handler(event, context):
    
    # Connect to Snowflake
    ctx = snowflake.connector.connect(
    user=SNOWFLAKE_USER,
    password=SNOWFLAKE_PASSWORD,
    account=SNOWFLAKE_URL,
    warehouse=SNOWFLAKE_WAREHOUSE,
    database=SNOWFLAKE_DATABASE,
    schema=SNOWFLAKE_SCHEMA,
    # authenticator='externalbrowser'  # Optionally specify an authenticator
    )
    cs = ctx.cursor()
    
    print('connected')
    
    s3 = boto3.client('s3')
        
    # Get the file name from the Lambda event
    file_name = unquote(event['Records'][0]['s3']['object']['key'])
    print(file_name)
    s3_path = f"s3://cleandata-snowflake/{file_name}"
    
    # Get the file object from S3
    file_obj = s3.get_object(Bucket="cleandata-snowflake", Key=file_name)
    # try:
    #     file_content = file_obj['Body'].read().decode('utf-8-sig')
    # except UnicodeDecodeError as e:
    file_content = file_obj['Body'].read().decode('utf-8', 'ignore')
        
        
    jobs = list(csv.DictReader(StringIO(file_content)))
    print(len(jobs))
    if 'totaljobs' in file_name:
        load_totalJobs(jobs, cs)
    else:
        print(len(jobs))
        load_indeed_jobs(jobs, cs)
    
    return {
        'statusCode': 200,
        'body': 'Data processing completed successfully.'
    
    }