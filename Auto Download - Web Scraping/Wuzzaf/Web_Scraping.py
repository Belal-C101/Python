import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest
from selenium import webdriver
import time

# Path to the Chrome WebDriver executable (change this path to match your setup)
webdriver_path = r'C:\Users\Mohamed\Downloads\chromedriver-win64chromedriver.exe'

driver = webdriver.Chrome()
driver.maximize_window()
job_titles = []
company_names = []
locations = []
job_skills = []
salary = []
skills_and_tools = []
links = []
page_num = 0
x = 1

while True:
    try :

        # use requests to fetch the url
        driver.get(f"https://wuzzuf.net/search/jobs/?a=hpb&q=python&start={page_num}")


        # save the page content/markup
        src = driver.page_source.encode('utf-8').strip()

        # creat soup object to parse the content
        soup = BeautifulSoup(src , "lxml")
        page_limit = int(soup.find("strong").text)
        print("Page" , x)
        x += 1

        if page_num > (page_limit // 15) :
            break

        # find the element contain the info we need
        # jop titles , jop skills , company names , location
        job_title = soup.find_all("h2" , {"class":"css-m604qf"})
        company_name = soup.find_all("a" , {"class":"css-17s97q8"})
        location = soup.find_all("span" , {"class":"css-5wys0k"})


        # loop over returned lists to extract needed info into other lists
        for i in range(len(job_title)) :
            job_titles.append(job_title[i].text)
            links.append(job_title[i].find("a").attrs['href'])
            company_names.append(company_name[i].text)
            locations.append(location[i].text)
       


        page_num += 1
    except :
        print("error occured")
        break


    # loop for entering site
for link in links :
    driver.get(link)
    src = driver.page_source.encode('utf-8').strip()
    soup = BeautifulSoup(src , "lxml")
    salaries = soup.find_all("span" , {"class":"css-4xky9y"})
    fourth_div = salaries[3]
    salary.append(fourth_div.text)
    time.sleep(2)
    


# creat csv file and fill wit info we get
file_list = [job_titles , company_names , locations , salary]
exported = zip_longest(*file_list)
with open("\Projects\VS Logs\general\Python\Web_Scraping\JOP.csv" , "w" , encoding='utf-8', newline='') as myfile :
    wr = csv.writer(myfile)
    wr.writerow(["Job Title" , "Company Name" , "Location" , "Salary"])
    wr.writerows(exported)
