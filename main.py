from src.crawler.job_crawler import SaraminCrawler

def main():
    crawler = SaraminCrawler()
    
    # 첫 3페이지 크롤링 (약 120개의 채용공고)
    all_jobs = []
    for page in range(1, 4):
        jobs = crawler.get_job_listings(page)
        all_jobs.extend(jobs)
        print(f"Crawled page {page}: {len(jobs)} jobs")
        time.sleep(1)  # 서버 부하 방지
    
    print(f"Total jobs crawled: {len(all_jobs)}")

if __name__ == "__main__":
    main()
