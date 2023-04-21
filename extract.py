from saveload import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import re
import spacy
nlp = spacy.load('en_core_web_md')

##########################scrape data from Linkedin#############################
service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
url = "https://www.linkedin.com/jobs/search/?currentJobId=3314905799&distance=25&f_JT=I&geoId=103644278&keywords=sde"
driver.get(url)

# calculate number of job total in Linkedin
no_of_jobs = int(driver.find_element(By.CSS_SELECTOR,'h1>span').get_attribute('innerText'))
i = 2
# loading more jobs if you scroll down the browser bar
while i <= int(no_of_jobs/25)+1: 
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    i = i + 1
    try:
        driver.find_element(By.XPATH, '/html/body/main/div/section/button').click()
        time.sleep(3)
    except:
        pass
        time.sleep(3)

job_lists = driver.find_element(By.CLASS_NAME,'jobs-search__results-list')
job_title = driver.find_elements(By.CLASS_NAME,'base-search-card__title')
job_company = driver.find_elements(By.CLASS_NAME,'hidden-nested-link')
job_location = driver.find_elements(By.CLASS_NAME,'job-search-card__location')
job_url = driver.find_elements(By.CLASS_NAME, 'base-card__full-link')

# get url
job_url_list = []
for i in job_url:
    job_url_list.append(i.get_attribute('href'))
# get title
job_title_list = []
for i in job_title:
    job_title_list.append(i.text)
# get company name and url
job_company_list = []
job_company_url_list = []
for i in job_company:
    job_company_list.append(i.text)
    job_company_url_list.append(i.get_attribute('href'))
# get work location
job_location_list = []
for i in job_location:
    job_location_list.append(i.text)

#######################scrape data from href we scraped#########################
job_type_list = []
job_function_list = []
job_describe_list = []
for i in job_url_list[:]:
    print(i)
    driver = webdriver.Chrome(service=service)
    driver.get(i)
    try:
        job_type = driver.find_element(By.CLASS_NAME, "description__job-criteria-list")
        job_type = job_type.find_elements(By.TAG_NAME, 'span')
        job_type_list.append(job_type[1].text)
        job_function_list.append(job_type[2].text)
        job_describe = driver.find_element(By.CLASS_NAME, "show-more-less-html__markup")
        job_describe_list.append(job_describe.text.strip())
    except:
        job_function_list.append('Not Clear')
        job_type_list.append('internship')
        job_describe_list.append('Not Clear')
    driver.close()
job_describe_lower_list = [i.lower().replace('\n','.') for i in job_describe_list]


# extract salary and skill
job_salary_list = []
job_skill_list = []
pattern_salary = r"(\$\d{1,3}(,\d{3})*(\.\d+)?\s*-\s*\$?\d{1,3}(,\d{3})*(\.\d+)?)|(\$\d{1,3}(,\d{3})*(\.\d+)?(\/(hr|hour))\s*-*(\s*\$?\d{1,3}(,\d{3})*(\.\d+)?(\/(hr|hour)))?)"
skills = ['java', 'c++', 'python', 'sql', 'matlab', 'aws']
for i in job_describe_lower_list[:]:
    matches = re.search(pattern_salary, i)
    if matches:
        job_salary_list.append(matches.group())
    else:
        job_salary_list.append('not declared')
    destext = []
    doc = nlp(i)
    totalSkill = ''
    for token in doc:
        destext.append(token.text)
    for skill in skills:
        if skill in destext:
            totalSkill = totalSkill + skill + ' '
    if totalSkill == '':
        totalSkill = 'not good at'
    job_skill_list.append(totalSkill)

#########################save the data to txt#############################
outFileName = {'title.txt': job_title_list,
               'company.txt': job_company_list,
               'location.txt': job_location_list,
               'joburl.txt': job_url_list, 
               'companyurl.txt': job_company_url_list,
               'function.txt': job_function_list,
               'type.txt': job_type_list,
               'describe.txt': job_describe_lower_list,
               'salary.txt': job_salary_list,
               'skill.txt': job_skill_list}
for i in outFileName.keys():
    outFile = open(i, 'w')
    saveCache(outFileName[i], outFile)
    outFile.close()

##########################save the data to json#############################
# load txt file
inFileName = {'title.txt': 'job_title_list',
               'company.txt': 'job_company_list',
               'location.txt': 'job_location_list',
               'joburl.txt': 'job_url_list', 
               'companyurl.txt': 'job_company_url_list',
               'function.txt': 'job_function_list',
               'type.txt': 'job_type_list',
               'describe.txt': 'job_describe_lower_list',
               'salary.txt': 'job_salary_list',
               'skill.txt': 'job_skill_list'}

for key, value in inFileName.items():
    inFile = open(key, 'r')
    exec(f"{value} = openCache(inFile)")
    inFile.close()

outFileName = {'title.txt': job_title_list,
               'company.txt': job_company_list,
               'location.txt': job_location_list,
               'joburl.txt': job_url_list, 
               'companyurl.txt': job_company_url_list,
               'function.txt': job_function_list,
               'type.txt': job_type_list,
               'describe.txt': job_describe_lower_list,
               'salary.txt': job_salary_list,
               'skill.txt': job_skill_list}

key = [i[:-4] for i in list(outFileName.keys())]
value = list(outFileName.values())

cache_list = []
for j in range(len(value[0])):
    cache_dict = {}
    for i in range(len(key)):
        cache_dict[key[i]] = value[i][j]
    cache_list.append(cache_dict)

save_cache(cache_list, 'cache.json')