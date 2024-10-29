
import sys
from fetch_page import fetch_page  
from parse_page import parse_page
from db_operations import insert_job_item, job_exists, get_all_jobs
from email_utils import send_job_email, send_no_jobs_found_email

URL = "https://recruiting2.ultipro.com/SPA1004AURA/JobBoard/93330e50-7b3a-4ba8-94f2-6f32360aa4e1/?q=&o=postedDateDesc"  # Replace with your target URL
KEYWORDS = ['programmer', 'developer', 'software', 'dev', 'cloud']

def keyword_filter(job):
    job_title_lower_case = job['title'].lower()
    return any(keyword in job_title_lower_case for keyword in KEYWORDS)

response = fetch_page(URL)
if not response: 
    print("Program exited with an error.")
    sys.exit(1)

emails_sent = 0
keyword_filtered_jobs = filter(keyword_filter, parse_page(response))
for job in keyword_filtered_jobs:
    if not job_exists(job):
        insert_job_item(job)
        send_job_email(job)
        emails_sent += 1
    else:
        print(f'Ignoring job post {job["id"]}, already tracked in DB.')

if emails_sent == 0:
    send_no_jobs_found_email()
