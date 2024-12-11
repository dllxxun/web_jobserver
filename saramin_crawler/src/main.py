# main.py
from crawler.job_crawler import SaraminCrawler


import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    crawler = SaraminCrawler()
    jobs = crawler.crawl_multiple_pages(start_page=1, end_page=5)
    
    print(f"\n크롤링 결과:")
    print(f"총 수집된 채용공고 수: {len(jobs)}")
    
    # 샘플 데이터 출력
    for idx, job in enumerate(jobs[:5], 1):
        print(f"\n채용공고 {idx}")
        print(f"제목: {job['title']}")
        print(f"회사: {job['company']}")
        print(f"위치: {job['location']}")
        print("-" * 50)

if __name__ == "__main__":
    main()
