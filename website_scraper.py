# website_scraper.py
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from urllib.parse import urlparse, urlunparse
import datetime
import os
import sys

class SmartSpider(CrawlSpider):
    name = 'smart_spider'

    def __init__(self, start_url, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.allowed_domains = [urlparse(start_url).netloc]
        self.start_urls = [start_url]
        self.visited_urls = set()
        self.rules = (
            Rule(LinkExtractor(allow=(), deny=(r'\?.*',), unique=True), callback='parse_page', follow=True),
        )
        super(SmartSpider, self)._compile_rules()

    def parse_page(self, response):
        cleaned_url = self._strip_query(response.url)
        if cleaned_url in self.visited_urls:
            return
        self.visited_urls.add(cleaned_url)

        title = response.xpath('//title/text()').get()
        texts = response.xpath('//p/text() | //h1/text() | //h2/text()').getall()
        images = [response.urljoin(src) for src in response.xpath('//img/@src').getall()]
        links = [response.urljoin(href) for href in response.xpath('//a/@href').getall()]

        texts = list({text.strip() for text in texts if text.strip()})
        images = list(set(images))
        links = list(set(links))

        yield {
            'url': cleaned_url,
            'title': title.strip() if title else '',
            'texts': texts,
            'images': images,
            'links': links
        }

    def _strip_query(self, url):
        parsed = urlparse(url)
        return urlunparse(parsed._replace(query='', fragment=''))


if __name__ == '__main__':
    url = sys.argv[1] if len(sys.argv) > 1 else 'https://quotes.toscrape.com/'

    domain = urlparse(url).netloc.replace('.', '_').replace('-', '_')
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{domain}_{timestamp}.json"
    full_path = os.path.join(output_dir, filename)

    process = CrawlerProcess(settings={
        'FEEDS': {
            full_path: {
                'format': 'json',
                'overwrite': True,
                'indent': 2
            }
        },
        'LOG_LEVEL': 'INFO',
        'DEPTH_LIMIT': 5,
        'CLOSESPIDER_PAGECOUNT': 100,
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'ROBOTSTXT_OBEY': True,
    })

    process.crawl(SmartSpider, start_url=url)
    process.start()

    # Output just the filename (used in Streamlit)
    print(full_path)
