from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from datetime import date, timedelta
import csv
import boto3

today_date = date.today()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach', True)
chrome_options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=chrome_options)

# URL = 'https://uk.indeed.com/jobs?q=data+engineer&l=London%2C+Greater+London&from=searchOnHP&vjk=b4dbd21f9ddb3a98'
URL = 'https://uk.indeed.com/jobs?q=junior+data+engineer&l=London%2C+Greater+London'
# URL = 'https://uk.indeed.com/jobs?q=junior+data+engineer&l=London%2C+Greater+London&fromage=14&vjk=a75060734fbe4da0'

# driver.get(URL)

jobs = []
MAX_JOBS = 50

def get_jobs():
    time.sleep(2)
    # job_cards = driver.find_elements(By.CSS_SELECTOR, value='#mosaic-jobResults.mosaic-zone li .resultContent')
    job_cards = driver.find_elements(By.CSS_SELECTOR, value='#mosaic-jobResults.mosaic-zone li .cardOutline')
    print(len(job_cards))

    for card in job_cards:
        title_element = card.find_element(By.CSS_SELECTOR, value='.jobTitle span')
        title = title_element.get_attribute('textContent')
        location_element = card.find_element(By.CSS_SELECTOR, value='.company_location div[data-testid="text-location"]')
        location = location_element.get_attribute('textContent')
        
        company_element = card.find_element(By.CSS_SELECTOR, value='.company_location span[data-testid="company-name"]')
        company_name = company_element.get_attribute('textContent')
        # posted_ago_el = card.find_element(By.CSS_SELECTOR, value='span.date')
        
        try:
            posted_ago_el = card.find_element(By.CSS_SELECTOR, value='span[data-testid="myJobsStateDate"]')
            # print(posted_ago)
            inner_span_text = posted_ago_el.find_element(By.CSS_SELECTOR, value='span').text.lower()
            outer_span_text = posted_ago_el.text.lower().replace(inner_span_text, '').strip()
            # print(outer_span_text)
        except:
            outer_span_text = '2 days ago'
        
        date_posted = today_date
        if 'today' in outer_span_text or 'just posted' in outer_span_text:
            pass
        elif 'day' in outer_span_text:
            if 'active' in outer_span_text:
                n_days_ago = int(outer_span_text[7:9])
            else:
                n_days_ago = int(outer_span_text[0:2])
            date_posted = today_date - timedelta(days=n_days_ago)
            
        date_posted = date_posted.strftime('%d-%m-%Y')
        # print(date_posted)
        
        try:
            salary_element = card.find_element(By.CSS_SELECTOR, value='.salary-snippet-container div')
            salary = salary_element.get_attribute('textContent')
        except:
            if 'senior' in title.lower():
                salary = '£60,000+ a year - Negotiable'
            elif 'junior' in title.lower():
                salary = '£25,000 - £35,000 a year'
            else: 
                salary = 'Competitive Salary - Negotiable'
                
        # link = card.find_element(By.LINK_TEXT, value=title).get_attribute('href')
        link_el = card.find_element(By.CSS_SELECTOR, value='.jobTitle a')
        link = link_el.get_attribute('href')
        job = {'job_title': title, 'location': location, 'company_name': company_name, 'salary': salary, 'date_posted': date_posted, 'link': link, 'skills': []}
        # print(job)
        jobs.append(job)
        if (len(jobs)) >= MAX_JOBS: return
        
        driver.execute_script('arguments[0].click()', link_el)
        time.sleep(4)
        # time.sleep(2)
        
        skills_el = []
        
        try:
            # print('Entering...')
            more_btn = driver.find_element(By.CSS_SELECTOR, value='div[aria-label="Skills"] div ul button')
            driver.execute_script('arguments[0].click()', more_btn)
            time.sleep(1)
            skills_el = driver.find_elements(By.CSS_SELECTOR, value='div[aria-label="Skills"] div ul li')
            skills_el.pop()
            # job['skills'] = skills_el
        except:
            # job['skills'] = driver.find_elements(By.CSS_SELECTOR, value='div[aria-label="Skills"] div ul li')
            skills_el = driver.find_elements(By.CSS_SELECTOR, value='div[aria-label="Skills"] div ul li')

        for i in range(len(skills_el)):
            skills_el[i] = skills_el[i].text

        if len(skills_el) > 0:
            job['skills'] = skills_el

    time.sleep(2)

    # next_el = driver.find_element(By.CSS_SELECTOR, value='a[aria-label="Next Page"]')
    # driver.execute_script('arguments[0].click()', next_el)
    # time.sleep(2)
    # try:
    #     close_pop_up = driver.find_element(By.CSS_SELECTOR, value='button[aria-label="close"]')
    #     driver.execute_script('arguments[0].click()', close_pop_up)
        
    #     next_el = driver.find_element(By.CSS_SELECTOR, value='a[aria-label="Next Page"]')
    #     driver.execute_script('arguments[0].click()', next_el)
    #     # driver.quit()
    #     job_cards = driver.find_elements(By.CSS_SELECTOR, value='#mosaic-jobResults.mosaic-zone li .cardOutline')
    #     title_element = job_cards[0].find_element(By.CSS_SELECTOR, value='.jobTitle span')
    #     title = title_element.get_attribute('textContent')
    #     print(title)
    # except:
    #     pass

def login_indeed():
    driver.get('https://secure.indeed.com/auth?hl=en_GB&co=GB&continue=https%3A%2F%2Fuk.indeed.com%2Fjobs%3Fq%3Djunior%2520data%2520engineer%26l%3DLondon%252C%2520Greater%2520London%26from%3DsearchOnHP&tmpl=desktop&from=gnav-util-jobsearch--indeedmobile&jsContinue=https%3A%2F%2Fuk.indeed.com%2Fjobs%3Fq%3Djunior%2520data%2520engineer%26l%3DLondon%2C%2520Greater%2520London%26from%3DsearchOnHP&empContinue=https%3A%2F%2Faccount.indeed.com%2Fmyaccess&_ga=2.83814806.1226575244.1705160808-2032313447.1705160808')

    email = 'mohammedaslam848@outlook.com'
    password = 'TestWebScrape848'
    
    email_input = driver.find_element(By.NAME, value='__email')
    email_input.send_keys(email)
    
    continue_btn = driver.find_element(By.CSS_SELECTOR, value='form#emailform button')
    continue_btn.click()
    time.sleep(4)
    input('Press enter after you have completed the captcha')
    # driver.find_element(By.NAME, value='__email').clear()
    try:
        continue_btn.click()
        time.sleep(2)
    except:
        pass
    
    pass_input = driver.find_element(By.NAME, value='__password')
    pass_input.send_keys(password)

    login_btn = driver.find_element(By.CSS_SELECTOR, value='form#loginform button[type="submit"]')
    login_btn.click()
    time.sleep(4)
    input('Press enter after you have completed the captcha password')

    try:
        pass_input = driver.find_element(By.NAME, value='__password')
        pass_input.send_keys(password)
        login_btn = driver.find_element(By.CSS_SELECTOR, value='form#loginform button[type="submit"]')
        login_btn.click()
    except:
        pass
    
    time.sleep(2)

    input('Two factor authentication completed')

    time.sleep(4)

login_indeed() # Login to indeed account
driver.get(URL)
time.sleep(3)
try:
    close_pop_up = driver.find_element(By.CSS_SELECTOR, value='button[aria-label="close"]')
    driver.execute_script('arguments[0].click()', close_pop_up)
except:
    pass

while True:
    get_jobs()
    if len(jobs) >= MAX_JOBS: break
    try:
        next_el = driver.find_element(By.CSS_SELECTOR, value='a[aria-label="Next Page"]')
        print(next_el.get_attribute('href'))
        driver.execute_script('arguments[0].click()', next_el)
        time.sleep(2)
        
        try:
            close_pop_up = driver.find_element(By.CSS_SELECTOR, value='button[aria-label="close"]')
            driver.execute_script('arguments[0].click()', close_pop_up)
        except:
            pass
        
    except:
        break

# driver.quit()
print(len(jobs))
# while True:
#     get_jobs()
#     next_el = driver.find_element(By.CSS_SELECTOR, value='a[aria-label="Next Page"]')
#     print(next_el.get_attribute('href'))
#     driver.execute_script('arguments[0].click()', next_el)
#     time.sleep(2)
    
#     try:
#         close_pop_up = driver.find_element(By.CSS_SELECTOR, value='button[aria-label="close"]')
#         driver.execute_script('arguments[0].click()', close_pop_up)
#     except:
#         pass

header = ['job_title', 'location', 'company_name', 'salary', 'link', 'date_posted', 'skills']
with open('indeed_jobs.csv', 'w') as f:
    writer = csv.DictWriter(f, fieldnames=header)
    writer.writeheader()
    for job in jobs:
        writer.writerow(job)
        
s3 = boto3.client('s3')
with open("indeed_jobs.csv", "rb") as f:
    s3.upload_fileobj(f, "dirty-data-skillnet", "OBJECT_NAME")