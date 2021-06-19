import requests
from bs4 import BeautifulSoup as bs4
import pandas as pd

class job_info:
    def __init__(self):
        self.companyName = '' # 회사 이름
        self.link = '' # 공고 링크
        self.position = '' # 정규직 or 계약직
        self.location = '' # 위치
        self.deadline = '' # 입사 최종 날짜
        self.condition = '' # 대졸 초졸
        self.salary = '' # 월급

    def print(format_job):
            print(f'company_name :{format_job.companyName}')
            print(f'link :{format_job.link}')
            print(f'position :{format_job.position}')
            print(f'location :{format_job.location}')
            print(f'deadline :{format_job.deadline}')
            print(f'condition :{format_job.condition}')
            print(f'salary :{format_job.salary}')

    def get_header(self):
        return ['company_name', 'link', 'position', 'location', 'deadline', 'condition', 'salary']

    def get_value(self):
        return [self.companyName, self.link, self.position, self.location, self.deadline, self.condition, self.salary]

    def get_value_as_dict(self):
        dict_form = {}
        for key, val in zip(self.get_header(), self.get_value()):
            dict_form[key] = val
        return dict_form

def get_job_info(job):
    format_job = job_info()
    try:
        format_job.companyName = job.find("div", class_="area_corp").find("a")['title'] 
    except:
        pass
    try:
        format_job.link = 'https://www.saramin.co.kr'+ job.find("div", class_="area_job").find("a")['href']
    except:
        pass
    job_condition = job.find("div", class_="job_condition")
    try:
        format_job.location = ' '.join([loc.text.strip() for loc in job_condition.find_all("a")])
    except:
        pass
    try:
        format_job.position = job_condition.find_all("span")[3].text.strip()
    except:
        pass
    try:
        format_job.condition = ' '.join([loc.text.strip() for loc in job_condition.find_all("span")[1:3]])
    except:
        pass
    try:
        format_job.salary = job_condition.find_all("span")[4].text.strip()
    except:
        pass
    try:
        format_job.deadline = job.find("div", class_="job_date").find("span").text.strip()
    except:
        pass
    return format_job

def get_jobs(soup):
    jobs = soup.find_all("div", class_="item_recruit")
    list_dict_job = []
    for job in jobs:
        format_job = get_job_info(job)
        # format_job.print()
        list_dict_job.append(format_job.get_value_as_dict())
    return list_dict_job

def read_url(url):
    response = requests.get(url)

    if response.status_code == 200:
        html = response.text
        soup = bs4(html, 'html.parser')
        return soup
    else:
        raise RuntimeError(f"Can't connect to the url {url}")

def crolling(word_input, FORMAT_URL = 'https://www.saramin.co.kr/zf_user/search/recruit'
):
    i = 1
    list_tot_dict_job = []
    while True:
        url = f"{FORMAT_URL}?searchword={word_input}&recruitPage={i}"
        url_text = read_url(url)
        if url_text.find("div", class_="info_no_result"):
            break
        else:
            print(url)
            list_dict_job = get_jobs(url_text)
            list_tot_dict_job.extend(list_dict_job)
        i += 1
    return list_tot_dict_job

def save_list_dict_job_to_csv(list_dict_job, word_input):
    df_job = pd.DataFrame(list_dict_job)
    d_csv = f'word_input-{word_input}.csv'
    df_job.to_csv(d_csv)
    return d_csv