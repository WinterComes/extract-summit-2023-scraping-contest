import json

import scrapy
from scrapy.http import Request
from word2number import w2n

from contest.items import ContestItem

def string_to_integer(s):
    # Define a dictionary to map string representations to integer values
    word_to_number = {
        'zero': 0,
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9
    }

    # Try to convert the input string to an integer, or return None if it's not in the dictionary
    return word_to_number.get(s.lower(), None)

class ContestSpiderSpider(scrapy.Spider):
    name = "contest_spider"
    allowed_domains = ["ducqocgbcrqftlrn-5umjfyjn4a-ew.a.run.app"]
    start_urls = ["http://ducqocgbcrqftlrn-5umjfyjn4a-ew.a.run.app/items", "http://ducqocgbcrqftlrn-5umjfyjn4a-ew.a.run.app/sitemap.xml"]

    def parse(self, response):

        if response.url == "https://ducqocgbcrqftlrn-5umjfyjn4a-ew.a.run.app/sitemap.xml":
            print("HASHAHSH")
            for url in response.xpath("//loc/text()").getall():
                yield Request(
                    url=url,
                    meta={"url_type": "pdp"},
                    headers={"User-Agent": "GoodRobot"}
                )
            return


        if response.meta.get("url_type") and response.meta.get("url_type") == "pdp":
            yield self.extract_detail(response)
            return

        for url in response.xpath("//*[contains(@href, 'item/')]/@href").getall():
            yield Request(
                url=response.urljoin(url),
                meta={"url_type": "pdp"},
                headers={"User-Agent": "GoodRobot"}
            )

        next_url = response.xpath("//*[contains(text(), '→')]/@href").get()

        if next_url:
            yield Request(
                url=response.urljoin(next_url),
            )

    def extract_detail(self, response):
        item = ContestItem()

        item["text"] = response.xpath("//pre/text()").get()
        item["item_id"] = response.xpath("//*[contains(text(), 'UUID')]/span/text()").get('').strip()
        stock_str = response.xpath("//*[contains(text(), 'Available')]/span/text()").get('').strip()
        item["stock"] = w2n.word_to_num(stock_str)

        # rating_url = response.xpath("//*[contains(text(), 'Rating')]/span/@data-price-url").get('').strip()
        #
        # if not rating_url:
        #     item["rating"] = response.xpath("//*[contains(text(), 'Rating')]/span/text()").get('').strip()
        #     return item


        return item


