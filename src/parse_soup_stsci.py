#All STSCI job posting are wrapped in a div with a class of "opportunity"
JOB_POSTING_SELECTOR=".opportunity"

#The key to the job will be the requisition number.
# Look for a span with an attribute "data-bind" and value of "text: RequisitionNumber()"
# The requisition number is a string and will be the inner text of this span.abs
ATTR_REQUISITION_KEY="data-bind"
ATTR_REQUISITION_VALUE="text: RequisitionNumber()"
REQUISITION_SELECTOR=f'span[{ATTR_REQUISITION_KEY}="{ATTR_REQUISITION_VALUE}"]' 

#The job title will be am anchor element with a attribute data-automation and a value of "job-title"
#The job title will be the inner HTML of this anchor.
#Conveniently, the href attribute is a link to the post, save this too!
ATTR_JOB_TITLE_KEY="data-automation"
ATTR_JOB_TITLE_VALUE="job-title"
JOB_TITLE_SELECTOR=f'a[{ATTR_JOB_TITLE_KEY}="{ATTR_JOB_TITLE_VALUE}"]'

#The job description will be in an attribute called data-automation with a value of "job-brief-description"
ATTR_JOB_DESCRIPTION_KEY="data-automation"
ATTR_JOB_DESCRIPTION_VALUE="job-brief-description"
JOB_DESCRIPTION_SELECTOR=f'div[{ATTR_JOB_DESCRIPTION_KEY}="{ATTR_JOB_DESCRIPTION_VALUE}"]'

def get_element_text(opportunity_element, selector):
    elements = opportunity_element.select(selector)
    if len(elements) > 0:
        return elements[0].text
    else:
        return None

def get_requisition_id(opportunity_element):
    return get_element_text(opportunity_element, REQUISITION_SELECTOR)

def get_job_title(opportunity_element):
    return get_element_text(opportunity_element, JOB_TITLE_SELECTOR)

def get_job_description(opportunity_element):
    return get_element_text(opportunity_element, JOB_DESCRIPTION_SELECTOR)

def get_link(opportunity_element):
    anchors = opportunity_element.select(JOB_TITLE_SELECTOR)
    if len(anchors) > 0:
        link = anchors[0].get('href')
        return f'https://recruiting2.ultipro.com${link}'
    else:
        return None

def get_job(opportunity_element):
    job = {
        "id": get_requisition_id(opportunity_element),
        "title": get_job_title(opportunity_element),
        "description": get_job_description(opportunity_element),
        "link": get_link(opportunity_element)
    }
    if all(job.values()):
        return job
    else: 
        return None

def filter_job(job):
    return bool(job)

def parse_soup_stsci(soup):
    opportunity_elements = soup.select(JOB_POSTING_SELECTOR)
    jobs = list(filter(filter_job, map(get_job, opportunity_elements)))
    return jobs