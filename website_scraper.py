import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from bs4 import BeautifulSoup
import os
import json


class UniversalSpider(scrapy.Spider):
    name = 'universal_spider'

    def __init__(self, url=None, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [url]
        self.items = []

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')

        # Extract relevant text content
        content = {
            "title": soup.title.string if soup.title else '',
            "headings": [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2', 'h3'])],
            "paragraphs": [p.get_text(strip=True) for p in soup.find_all('p')],
            "links": [{"text": a.get_text(strip=True), "href": a.get('href')} for a in soup.find_all('a', href=True)]
        }

        self.items.append(content)
        yield content


def run_scraper(url):
    output_file = "output.json"

    if os.path.exists(output_file):
        os.remove(output_file)

    configure_logging({'LOG_LEVEL': 'ERROR'})  # Clean logs

    process = CrawlerProcess(settings={
        "FEED_FORMAT": "json",
        "FEED_URI": output_file,
        "USER_AGENT": "Mozilla/5.0 (compatible; SmartScraperBot/1.0)",
        "DOWNLOAD_TIMEOUT": 10
    })

    process.crawl(UniversalSpider, url=url)
    process.start()

    return output_file
