from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
import os
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

password = os.environ.get('LINKEDIN_PASSWORD')
username = os.environ.get('LINKEDIN_USERNAME')

def initialize():
    ### load selenium driver
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(log_path='./Log/geckodriver.log', options = options)
    return driver

def login(driver):
    driver.get('https://linkedin.com/')
    sleep(1)
    ### get username and password input boxes path
    username = driver.find_element("xpath", '//*[@id="session_key"]')
    password = driver.find_element("xpath", '//*[@id="session_password"]')

    ### input the email id and password
    username.send_keys("vijayiyer7@gmail.com")   ## take from env or config file
    password.send_keys("EasyToRemember@1")  ## take from env or config file

    ### click the login button
    login_btn = driver.find_element\
            ("xpath", "//button[@class='sign-in-form__submit-button']")
    login_btn.click()
    sleep(5)

def get_num_job_pages(driver, src):
    soup = BeautifulSoup(src, "lxml")
    pages_element = soup.find('ul', class_='artdeco-pagination__pages')
    num_pages = len(pages_element.find_all('li', class_='artdeco-pagination__indicator'))
    return num_pages

def get_saved_jobs_in_page(driver, src):
    soup = BeautifulSoup(src, "lxml")
    saved_jobs = soup.find_all('li', class_='reusable-search__result-container')
    return saved_jobs

def get_job_details_in_page(driver, saved_jobs):
    saved_jobs_list = []
    
    for job in saved_jobs:
        saved_jobs_dict = dict()
        job_title_element = job.find('span', class_='entity-result__title-text')
        job_title_link = job_title_element.find('a', class_='app-aware-link')
        company = job.find('div', class_='entity-result__primary-subtitle')
        saved_jobs_dict['title'] = job_title_link.text.strip()
        saved_jobs_dict['link'] = job_title_link['href']
        saved_jobs_dict['job_id'] = job_title_link['href'].split('/')[-2]
        saved_jobs_dict['company'] = company.get_text().strip()
        saved_jobs_dict['company_thumbnail'] = get_job_image(driver, job)
        # print('{}:{}:{}:{}:{}'.format(saved_jobs_dict['title'].strip(), saved_jobs_dict['link'].strip(), saved_jobs_dict['company'], saved_jobs_dict['company_thumbnail'], saved_jobs_dict['job_id']))
        # print('\n')
        saved_jobs_list.append(saved_jobs_dict)
    
    return saved_jobs_list

def get_job_image(driver, job):
    img_wrapper = job.find('div', class_='ivm-view-attr__img-wrapper')
    img_url = img_wrapper.find('img')
    return img_url["src"]

def extract_jobs(driver, url, num_jobs = 0, count = 0):
    
    print(url+"?start={}".format(num_jobs))
    driver.get(url+"?start={}".format(num_jobs))
    sleep(1)
    src = driver.page_source
    saved_jobs = get_saved_jobs_in_page(driver, src)
    saved_jobs_list = get_job_details_in_page(driver, saved_jobs)
    print('number of saved jobs in page = {}'.format(len(saved_jobs)))
    if len(saved_jobs) > 0 and count < 5:
        print(num_jobs + len(saved_jobs), count + 1)
        saved_jobs_list = saved_jobs_list + extract_jobs(driver, url, num_jobs + len(saved_jobs), count + 1)
    
    print(len(saved_jobs_list))
    return saved_jobs_list
    
def extract_all_saved_jobs():
    saved_jobs_list = []
    try:
        driver = initialize()
        login(driver)
        saved_jobs_list = extract_jobs(driver, "https://linkedin.com/my-items/saved-jobs")
        
    except Exception as e:
        print(e)
    finally:
        driver.close()
        return saved_jobs_list


if __name__== "__main__":
    extract_all_saved_jobs()
