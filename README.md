# skill-map-ETL

## Data Engineer Skills Identification Project

### Overview

This project aims to assist aspiring data engineers in understanding the various skills required for the profession. By web scraping job postings from popular job sites like Indeed and TotalJobs, the project identifies and recognizes different skills demanded in the field of data engineering. The extracted job data includes crucial information such as job title, recruiter, salary, and most importantly, job skills. The project integrates with AWS for seamless data processing and implements an ETL pipeline to clean, transform, and load the data into a Snowflake database for further analysis.

### Features

- **Web Scraping**: Utilizes Python scripts to scrape job postings from Indeed and TotalJobs websites. Each scrape fetches 50 job listings at a time.
- **Data Extraction**: Extracts essential job data including job title, recruiter, salary, and job skills from the scraped web pages.
- **AWS Integration**: Automatically sends the extracted job data to an AWS S3 bucket, triggering an ETL pipeline/process.
- **ETL Pipeline**: Implements an ETL process within AWS. The process involves:
  - Transformation Lambda Function: Cleans and corrects the format of the job data CSV file, sending it to another S3 bucket.
  - Load Lambda Function: Extracts data from the cleaned CSV file and loads it into a Snowflake database with a predefined schema.
- **Snowflake Database**: Stores job-related data with schemas for jobs and skills. Schema includes fields such as job ID, job title, recruiter, salary, skill ID, and skill name.
- **Data Analysis**: Utilizes POWER BI to analyze job skills and create a skills map of data engineering jobs. Additionally, performs analysis and creates dashboards based on the data.
- **Automation**: The ETL pipeline is automated to run weekly at a specified time, ensuring regular updates and analysis of job postings.

### Setup Instructions

1. Clone the repository from GitHub.
2. Install the necessary dependencies by running `pip install -r requirements.txt`.
3. Configure AWS credentials for S3 bucket access.
4. Set up Snowflake database with the provided schema.
5. Ensure proper configuration of AWS Lambda functions for ETL pipeline.
6. Run the main Python script to initiate the web scraping process and trigger the ETL pipeline.

### Project Structure

```
project-root/
│
├── src/
│   ├── etl-lambda/
│   │   ├── extract_transform_lambda/
│   │   │   ├── lambda_function.py         # Python script for transformation Lambda function
│   │   │   ├── skills_list.py             # Python script for extracting skills list
│   │   │   └── TJClean.py                 # Python script for cleaning TotalJobs data
│   │   │
│   │   └── load_jobs_lambda/
│   │       └── lambda_function.py         # Python script for load Lambda function
│   │
│   └── web-scraping/
│       ├── indeed-job-summary.py          # Python script for scraping job summaries from Indeed
│       └── total-jobs-scrape.py           # Python script for scraping job listings from TotalJobs
│
├── config/
│   └── aws_credentials.json               # AWS credentials configuration file
│
├── requirements.txt                       # List of Python dependencies
│
└── README.md                              # Project documentation

```

### Project Infrastructure & Architecture

Below is the architectural diagram illustrating the flowchart of the entire project:

![Skills_Map Jobs_Scrape ETL Architecture](https://github.com/hassan848/skill-map-ETL/assets/72468804/2e5a5958-89a4-4dd5-a686-37da85a08ac2)

### Database Schema

The Snowflake database used in this project has the following schema:

- **JOBS**:
  - **JOB_ID**: Unique identifier for each job posting.
  - **DATE_POSTED**: Date when the job was posted.
  - **JOB_TITLE**: Title of the job.
  - **RECRUITER**: Recruiter or company offering the job.
  - **SALARY**: Salary offered for the job.

- **SKILLS**:
  - **SKILL_ID**: Unique identifier for each skill.
  - **SKILL_NAME**: Name of the skill.

- **JOB_SKILLS**:
  - **JOB_ID**: Foreign key referencing the job ID in the JOBS table.
  - **SKILL_ID**: Foreign key referencing the skill ID in the SKILLS table.

### Analysis

You can find detailed analysis and insights in the accompanying POWER BI dashboard. Check out the screenshot below for a glimpse of the skills map and trends in data engineering job postings.

[![POWER BI Dashboard](path_to_screenshot)](path_to_full_dashboard)
