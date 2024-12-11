import requests
from bs4 import BeautifulSoup
import logging

class SaraminCrawler:
    def __init__(self):
        self.base_url = "https://www.saramin.co.kr/zf_user/search/recruit"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def crawl_multiple_pages(self, start_page=1, end_page=5):
        all_jobs = []
        for page in range(start_page, end_page + 1):
            try:
                response = requests.get(
                    self.base_url, 
                    params={'recruitPage': page}, 
                    headers=self.headers
                )
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                job_items = soup.select('.item_recruit')

                for item in job_items:
                    try:
                        title = item.select_one('.job_tit a').text.strip() if item.select_one('.job_tit a') else 'N/A'
                        company = item.select_one('.corp_name a').text.strip() if item.select_one('.corp_name a') else 'N/A'
                        location = item.select_one('.job_condition span:first-child').text.strip() if item.select_one('.job_condition span:first-child') else 'N/A'
                        deadline = item.select_one('.job_date .date').text.strip() if item.select_one('.job_date .date') else 'N/A'

                        all_jobs.append({
                            'title': title,
                            'company': company,
                            'location': location,
                            'deadline': deadline
                        })
                    except Exception as e:
                        logging.error(f"Error parsing job item: {e}")
                        continue

            except Exception as e:
                logging.error(f"Error on page {page}: {e}")

        return all_jobs
