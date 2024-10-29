import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def load_secret(secret_name, default=None):
    """Helper function to load secrets based on the environment"""
    environment = os.getenv("ENV", "development")
    if environment == "production":
        # In production, assume AWS injects secrets as environment variables
        return os.getenv(secret_name, default)
    else:
        # In development, use Docker secrets mounted as files
        try:
            with open(f"/run/secrets/{secret_name.lower()}", "r") as file:
                return file.read().strip()
        except FileNotFoundError:
            return default

def send_email(subject, text_body, html_body):
    # Set up email details

    email_user = load_secret("EMAIL_USER")
    email_password = load_secret("EMAIL_PASSWORD")  # App Password
    email_recipient = load_secret("EMAIL_RECIPIENT")
    
    # Create the email content
    msg = MIMEMultipart("alternative")
    msg["From"] = email_user
    msg["To"] = email_recipient
    msg["Subject"] = subject

    # Attach body with UTF-8 encoding
    msg.attach(MIMEText(text_body, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(email_user, email_password)
            server.sendmail(email_user, email_recipient, msg.as_string())
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")

def build_job_email_subject(job):
    stripped_title = job['title']
    return f"New STSCI job posted - {stripped_title}"

def build_job_email_body_text(job):
    title = job['title']
    description = job['description']
    link = job['link']
    email_body = f"""Hey John!,
    
A new software job has been posted at STSCI.

Title: {title}

Description: {description}

Link: {link}

Good Luck!

-jobfinder
    """
    return email_body

def build_job_email_body_html(job):
    title = job['title']
    description = job['description']
    link = job['link']
    email_body = f"""\
<html>
    <body>
        <p>Hey John!</p>
        <p>A new software job has been posted at STSCI.</p>
        <p><b>Title: </b>{title}</p>
        <p><b>Description: </b>{description}</p>
        <a href={link}><b>Apply Here!</b></a>
        <p>Good Luck!</p>
        <p>-jobfinder</p>
    </body
</html>
    """
    return email_body

def send_job_email(job):
    subject = build_job_email_subject(job)
    text_body = build_job_email_body_text(job)
    html_body = build_job_email_body_html(job)
    send_email(subject, text_body, html_body)

def send_no_jobs_found_email():
    subject = "No New STSCI Jobs Found - Job Finder Run Confirmation"
    body_text = """Hey John,

Your jobfinder application successfully ran and scraped the STSCI job board but no new positions were found matching your list of keywords.

Apologies,

-jobfinder
    """
    body_html = """\
<html>
<body>
<p>Hey John,</p>
<p>Your jobfinder application successfully ran and scraped the STSCI job board but no new positions were found matching your list of keywords.</p>
<p>Apologies,</p>
<p>-jobfinder</p>
</body>
</html>
"""
    send_email(subject, body_text, body_html)