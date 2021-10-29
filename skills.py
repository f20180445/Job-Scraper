#importing all the required libraries
import time
import requests
import json
import pandas as pd
from collections import Counter

#lists to store the data for every job post - index 0 has data for the first job post and so on
company_arr=[]
description_arr=[]
experience_arr=[]
location_arr=[]
salary_arr=[]
skills_arr=[]
all_skills=[]

#function to create the URL endpoint which gives the data. Designation and page number filters are applied here
#returns the url to scrape
def create_url(designation, page_number):
    pre = designation.strip().replace(" ","-")
    url = f"https://www.naukri.com/jobapi/v3/search?noOfResults=20&urlType=search_by_keyword&searchType=adv&keyword={designation}&pageNo={page_number}&k={designation}&seoKey={pre}-jobs-{page_number}&src=jobsearchDesk&latLong="
    #the API url was figured out from network request made by naukri.com to fetch the data
    return url

#function that hits the URL and returns the response
def get_response(url):
    headers_dict = {"appid": "109", "systemid":"109"} #figured out from the network request for API call used by Naukri.com
    page_response = requests.get(url,headers=headers_dict)

    if page_response.status_code>=400:
        return "Invalid Response"

    page_json = json.loads(page_response.text)
    return page_json

#function to append the data from the response to the lists created earlier
#returns None
def fill_data(page_json):
    #On one page (in one API call) we have 20 job posts. It can be changed from the API call.
    for i in range(20): #20 job posts on one page
        company=page_json['jobDetails'][i]['companyName']
        description=page_json['jobDetails'][i]['jobDescription']
        experience=page_json['jobDetails'][i]['placeholders'][0]['label']
        salary=page_json['jobDetails'][i]['placeholders'][1]['label']
        location=page_json['jobDetails'][i]['placeholders'][2]['label']
        skills=[]
        s=page_json['jobDetails'][i]['tagsAndSkills']
        skills.append(s) #skills are stored as a list

        skill_separator = s.split(',')
        for skill in skill_separator:
            all_skills.append(skill)

        company_arr.append(company)
        description_arr.append(description)
        experience_arr.append(experience)
        salary_arr.append(salary)
        location_arr.append(location)
        skills_arr.append(skills)

#function to create a dataframe after the lists are appended with the data
#returns the dataframe
def create_df_job_details():
    dict_job_details = {
    "Company":company_arr,
    "Job Description":description_arr,
    "Experience":experience_arr,
    "Salary":salary_arr,
    "Location":location_arr,
    "Key Skills":skills_arr
    }
    job_details = pd.DataFrame(dict_job_details)

    return job_details

#function to find the frequency of skills occuring in the jobs
def create_df_skill_frequency():
    dict_freq_skills = dict(Counter(all_skills))
    frequency_skills = pd.DataFrame(dict_freq_skills, index=["Frequency"])
    frequency_skills=(frequency_skills.T)

    return frequency_skills

#function to convert the dataframe to an excel file
def create_excel(job_details, frequency_skills):
    job_details.to_excel("job_details.xlsx", index=False, sheet_name="Job Details")
    frequency_skills.to_excel("frequency_skills.xlsx", sheet_name="Frequency Of Skills")

#main method that takes designation and number of pages as input and calling the functions in appropriate order
def main():
    designation = input("Enter Designation: ")
    number_of_pages = int(input("Enter number of pages to scrape: "))
    for page_number in range(1,number_of_pages+1): #making API calls page by page
        url=create_url(designation, page_number)
        page_json=get_response(url)
        if page_json=='Invalid Response': #if status code is >=400
            print("Invalid Response")
            break
        elif page_json['noOfJobs']==0: #if no results found from search
            print("Jobs Not Found")
            break
        fill_data(page_json)

    job_details = create_df_job_details()
    frequency_skills = create_df_skill_frequency()
    create_excel(job_details, frequency_skills)

if __name__ == '__main__':
    main()
