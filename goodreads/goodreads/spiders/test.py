
import scrapy
import re
from dateparser.search import search_dates

class Publish(scrapy.Spider):
    name = "test"
    start_urls = ["https://www.goodreads.com/book/show/9918083-goliath"]
    def parse(self, response):
        details = response.xpath('//div[@id="details"]/div/nobr/text()').get()
        if details == None:
            path = response.xpath('//div[@id="details"]/*')[1]
            details = path.xpath('text()').get()
        pub = search_dates(details)
        if pub is None:
            details = response.xpath('//div[@id="details"]/*')[1].xpath('text()').get()
            pub = search_dates(details)
        pub = pub[0][0]
        yield{
            "y" : pub
        }
        