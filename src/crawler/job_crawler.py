import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

class SaraminCrawler:
    def __init__(self):
        self.base_url = "https://www.saramin.co.kr/zf_user/search/recruit"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def get_job_listings(self, page=1):
        params = {
            'searchType': 'search',
            'recruitPage': page,
            'recruitSort': 'relation',
            'recruitPageCount': '40'
        }
        
        try:
            response = requests.get(self.base_url, params=params, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            job_list = []
            job_items = soup.select('.item_recruit')
            
            for item in job_items:
                job_data = {
                    'title': item.select_one('.job_tit a').text.strip(),
                    'company': item.select_one('.company_nm a').text.strip(),
                    'location': item.select_one('.job_condition span:first-child').text.strip(),
                    'experience': item.select_one('.job_condition span:nth-child(2)').text.strip(),
                    'education': item.select_one('.job_condition span:nth-child(3)').text.strip(),
                    'url': 'https://www.saramin.co.kr' + item.select_one('.job_tit a')['href'],
                    'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                job_list.append(job_data)
            
            return job_list
            
        except Exception as e:
            print(f"Error crawling page {page}: {str(e)}")
            return []

    def get_job_detail(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            detail_data = {
                'description': soup.select_one('.job_detail_content').text.strip(),
                'requirements': soup.select_one('.job_requirements').text.strip() if soup.select_one('.job_requirements') else '',
                'benefits': soup.select_one('.job_benefits').text.strip() if soup.select_one('.job_benefits') else ''
            }
            
            return detail_data
            
        except Exception as e:
            print(f"Error crawling detail page: {str(e)}")
            return None
    def verify_crawling_results(job_list):
        print(f"총 수집된 채용공고 수: {len(job_list)}")
    
        for idx, job in enumerate(job_list[:5], 1):
            print(f"\n채용공고 {idx}")
            print(f"제목: {job.get('title', 'N/A')}")
            print(f"회사: {job.get('company', 'N/A')}")
            print(f"위치: {job.get('location', 'N/A')}")
            print("-" * 50)


