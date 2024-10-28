
import sys
from fetch_page import fetch_page  
from parse_page import parse_page
from db_operations import insert_job_item, job_exists

URL = "https://recruiting2.ultipro.com/SPA1004AURA/JobBoard/93330e50-7b3a-4ba8-94f2-6f32360aa4e1/?q=&o=postedDateDesc"  # Replace with your target URL
KEYWORDS = ['programmer', 'developer', 'software', 'dev', 'cloud']

def keyword_filter(job):
    job_title_lower_case = job['title'].lower()
    return any(keyword in job_title_lower_case for keyword in KEYWORDS)

response = fetch_page(URL)
if not response: 
    print("Program exited with an error.")
    sys.exit(1)

keyword_filtered_jobs = filter(keyword_filter, parse_page(response))
for job in keyword_filtered_jobs:
    if not job_exists(job):
        insert_job_item(job)
        ## TODO: Send email!
    else:
        print(f'Ignoring job post {job["id"]}, already tracked in DB.')
