import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os
import json
import sys
from datetime import datetime

class QuoteSpider(scrapy.Spider):
    name = "quotes"

    def __init__(self, url='', **kwargs):
        super().__init__(**kwargs)
        self.url = url
        self.results = []

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response):
        for quote in response.css("div.quote"):
            self.results.append({
                'text': quote.css("span.text::text").get(),
                'author': quote.css("small.author::text").get(),
                'tags': quote.css("div.tags a.tag::text").getall(),
            })

def run_scraper(url):
    """Run the scraper for a given URL and return path to output JSON file."""
    os.makedirs("outputs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_file = f"outputs/output_{timestamp}.json"

    # Prepare settings
    settings = get_project_settings()
    settings.set('LOG_ENABLED', False)  # Optional: turn off logs

    process = CrawlerProcess(settings)
    process.crawl(QuoteSpider, url=url)  # ✅ Correct usage
    process.start()

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(process.spider.results, f, ensure_ascii=False, indent=2)

    return output_file

# CLI usage
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Please provide a URL to scrape.")
        sys.exit(1)
    
    url = sys.argv[1]
    output_file = run_scraper(url)
    print(output_file)
