"""
@author: DAO HONG QUAN - 20176850
"""

import scrapy
import re
from dateparser.search import search_dates


class Publish(scrapy.Spider):
    name = "books"

    start_id = 12080001
    end_id = 12100001



    amount = list(range(start_id,end_id))
    start_urls = ["https://www.goodreads.com/book/show/{}".format(i) for i in amount]



    def parse(self, response):

        bookID = response.request.url[36:]
        if bookID.find(".") == -1:
            bookID = bookID.split("-")[0]
        else:
            bookID = bookID.split(".")[0]

        title = response.xpath('//h1[@id="bookTitle"]/text()').get()
        title = title.strip()

        authors_list = []
        for author in response.xpath('//div[@id="bookAuthors"]/span[@itemprop="author"]/div[@class="authorName__container"]'):
            authors_list.append(author.xpath('a/span/text()').get())
        authors = ', '.join(authors_list)

        details = response.xpath('//div[@id="details"]/div/nobr/text()').get()
        if details == None:
            path = response.xpath('//div[@id="details"]/*')[1]
            details = path.xpath('text()').get()
        pub = search_dates(details)
        if pub is None:
            details = response.xpath('//div[@id="details"]/*')[1].xpath('text()').get()
            pub = search_dates(details)
        pub = pub[0][0]

        genre = response.css('div.rightContainer div.stacked div.h2Container a::attr(href)').get().split('/')[-1]

        series = response.xpath('//h2[@id="bookSeries"]/a/text()').get()
        if series is not None:
            series = series.strip()
            if series.startswith('(') and series.endswith(')'):
                series = series[1:-1]
            series = series.split(' #')[0]

        rate = response.xpath('//div[@id="bookMeta"]/span[@itemprop="ratingValue"]/text()').get()
        rate = rate.strip()

        rater = response.xpath('//div[@id="bookMeta"]/*')[6].xpath('meta/@content').get()

        review = response.xpath('//div[@id="bookMeta"]/*')[8].xpath('meta/@content').get()

        page = response.xpath('//div[@id="details"]/div/span[@itemprop="numberOfPages"]/text()').get()
        if page is not None:
            for spage in page.split():
                if spage.isdigit():
                    page = spage
                    break

        bookFormat = response.xpath('//div[@id="details"]/div/span[@itemprop="bookFormat"]/text()').get()

        lang = response.xpath('//div[@id="bookDataBox"]/div[@class="clearFloats"]/div[@itemprop="inLanguage"]/text()').get()

        js = response.xpath('//script[contains(.,"renderRatingGraph")]/text()').extract_first()
        m = re.search(r"[^[]*\[([^]]*)\]",js)
        num = re.findall(r'-?\d+\.?\d*',m.group(1))

        yield {
            'BookID' : bookID,
            'Title' : title,
            'Author' : authors,
            'Rating' : rate,
            'Number of raters' : rater,
            '5 stars' : num[0],
            '4 stars' : num[1],
            '3 stars' : num[2],
            '2 stars' : num[3],
            '1 star'  : num[4],
            'Number of reviewers' : review,
            'Pages' : page,
            'PublishDate' : pub,
            'Book format' : bookFormat,
            'Language' : lang,
            'GenreLink' : genre,
            'Series' : series
            }

        del title
        del author
        del authors_list
        del authors
        del details
        del genre
        del pub
        del series
        del rate
        del rater
        del review
        del page
        del bookFormat
        del lang
        del js
        del num
        del m
