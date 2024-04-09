import re
from skills_list import skills_list
import csv
from io import StringIO

# open CSV file
# iterate through lines and parse through through text
# correctly enter cleaned up text into dictionary
# append dictionary to list
# use job desc to create skills list for job
# add skills list to dictionary
# return list

job_list2 = []

def extract_figures(text):
    #check for 'per day' text
    # check for 'hour'
    # else:
        # return int or ints 
    if 'per day' in text or 'daily' in text:
        return 'daily rate'
    elif 'hour' in text or 'hourly' in text:
        return 'hourly rate'
    else:
        try:
            # Regular expression pattern to match figures
            pattern = r'£\d+(?:,\d+)?(?:\.\d+)?'
            figures = re.findall(pattern, text)
            return [float(figure.replace('£', '').replace(',', '')) for figure in figures]
        except:
            return [None]

    

def contains_per_day(text):
    return 'per day' in text.lower()

def clean_text(text):
    cleaned_text = text.strip('"').replace('\n', ' ')
    cleaned_text = cleaned_text.replace('TITLE:', '')
    cleaned_text = cleaned_text.replace('SALARY:', '')
    cleaned_text = cleaned_text.replace('RECRUITER:', '')
    cleaned_text = cleaned_text.replace('DATE:', '')
    cleaned_text = cleaned_text.replace('LINK:', '')
    cleaned_text = cleaned_text.replace('JOB DESC:', '')
    cleaned_text = cleaned_text.replace('sSCRAPE', '')
    cleaned_text = cleaned_text.strip()

    return cleaned_text


def parse_csv(file_path):
    job_list = []
   
   # Get the file object from S3
    # file_obj = s3.get_object(Bucket=source_bucket, Key=key)
    # file_content = file_obj['Body'].read().decode('utf-8')
    
    # Parse CSV content
    csvreader = csv.reader(StringIO(file_path), delimiter='|')
    next(csvreader)  # Skip the header row
    
    job_list = []
    
    # Iterate through each row
    for row_number, row in enumerate(csvreader, start=1):
        if len(row) < 7:
            print(f"Warning: Row {row_number} has fewer columns than expected.")
            continue
    
        # Clean and process each row
        cleaned_row = [clean_text(item) for item in row]
        data_dict = {
            'TITLE': cleaned_row[0],
            'SALARY': extract_figures(cleaned_row[1]),
            'RECRUITER': cleaned_row[2],
            'POSTDATE': cleaned_row[3],
            'HREF': cleaned_row[4],
            'JOB_DESC': cleaned_row[5],
            'SCRAPE_DATE': cleaned_row[6],
            'SKILLS': skill_search(cleaned_row[5])
        }
        job_list.append(data_dict)

    # Do something with the job_list, like saving to a database or another S3 bucket
    # print(job_list)
   
#   with open(file_path, newline='', encoding='utf-8') as csvfile:
#         csvreader = csv.reader(csvfile, delimiter='|')
#         next(csvreader)  # Skip the header row

#         for row_number, row in enumerate(csvreader, start=1):
#             if len(row) < 7:
#                 print(f"Warning: Row {row_number} has fewer columns than expected.")
#                 continue

#         # for row in csvreader:
#             cleaned_row = [clean_text(item) for item in row]
#             data_dict = {
#                 'TITLE': cleaned_row[0],
#                 'SALARY': extract_figures(cleaned_row[1]),
#                 'RECRUITER': cleaned_row[2],
#                 'POSTDATE': cleaned_row[3],
#                 'HREF': cleaned_row[4],
#                 'JOB_DESC': cleaned_row[5],
#                 'SCRAPE_DATE': cleaned_row[6],
#                 'SKILLS': skill_search(cleaned_row[5])
#             }
#             job_list.append(data_dict)
            
    return job_list
   
def skill_search(large_string):

       words = large_string.split()
       words = re.findall(r'\b\w+\b', large_string.lower())

    
       matching_words = set()

       for word in words:
           if word in skills_list:
               matching_words.add(word)
        
       return(matching_words)