# Job-Scraper
Takes Job Designation and Number of Pages to scrape as Input and stores results in Excel

Hey folks, thanks for providing this problem statement.<br>
Hitting the URL and parsing HTML using bs4 wasn't working on Naukri.com as it's rendered using JS, so had to figure out a workaround.<br>
The workaround was to find the API being called by Naukri.com to fetch the data using Network in Dev Tools and using appropriate headers to hit the API.

Dependencies used in the program-
time, requests, json, pandas, collections

The script is created on Python 3.8.2
On running the script in Python, two inputs would be asked - <br>1. Designation and <br>2. Number of Pages to Scrape

Example-<br>
Enter Designation: software developer<br>
Number of Pages to scrape: 5

TWO Excel Files would be created in the same folder as the script-<br>
1. job_details.xlsx - which has the details like - Company Name, Job Description, Experience Required, Salary, Location, Skills<br>
2. frequency_skills.xlsx - which has the name of the skill mapped to the number of times the skill occurs for that search

NOTE - Scraping more pages would take longer time. Scraping 20 pages would take around a minute.
