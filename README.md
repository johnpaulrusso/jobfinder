### Space Job Finder

This application, when complete, will run nightly on AWS ECS to scrape the STSCI job board and email me with any new software job postings.
In the future I plan to add additional job boards to the application.

Currently the application simple scrapes the job postings and writes the title, description, and link to a dynamoDB instance.

I am writing this application for several purposes:
1.) I want a job at STSCI.
2.) Some of those jobs require Python experience.
3.) Some of those jobs require AWS experience.