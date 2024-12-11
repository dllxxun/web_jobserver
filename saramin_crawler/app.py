from flask import Flask, render_template
from src.crawler.job_crawler import SaraminCrawler  # 경로 확인

app = Flask(__name__)

@app.route('/')
def index():
    try:
        crawler = SaraminCrawler()
        jobs = crawler.crawl_multiple_pages(start_page=1, end_page=5)
        return render_template('index.html', jobs=jobs)
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
