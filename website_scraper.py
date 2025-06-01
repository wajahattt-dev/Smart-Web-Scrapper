import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import sys
import json
import os

class QuoteSpider(scrapy.Spider):
    name = "quotes"

    def __init__(self, url=None, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [url]
        self.items = []

    def parse(self, response):
        self.logger.info(f"Parsing URL: {response.url}")
        for quote in response.css("div.quote"):
            item = {
                'text': quote.css("span.text::text").get(),
                'author': quote.css("small.author::text").get(),
                'tags': quote.css("div.tags a.tag::text").getall(),
            }
            self.items.append(item)
            yield item

def run_scraper(url):
    output_file = "output.json"

    if os.path.exists(output_file):
        os.remove(output_file)

    process = CrawlerProcess(settings={
        "LOG_LEVEL": "INFO",
        "FEED_FORMAT": "json",
        "FEED_URI": output_file
    })

    process.crawl(QuoteSpider, url=url)
    process.start()

    return output_file

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python website_scraper.py <URL>")
    else:
        result = run_scraper(sys.argv[1])
        print(result)
