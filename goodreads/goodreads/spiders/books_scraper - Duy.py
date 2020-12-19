# -*- coding: utf-8 -*-
"""

@author: DAO HONG QUAN - 20176850
"""

import scrapy
from dateparser.search import search_dates


class Publish(scrapy.Spider):
    name = "books_d"

    start_id = 400001
    end_id = 500001
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
        year = pub[0][0]
        year = year[-4:]
        
        genre = response.css('div.rightContainer div.stacked div.h2Container a::attr(href)').get()
        
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
        yield {
            'BookID' : bookID,
            'Title' : title,
            'Author' : authors,
            'Rate' : rate,
            'Raters' : rater,
            'Reviewers' : review,
            'Pages' : page,
            'PublishYear' : year,
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
        del year
        del series
        del rate
        del rater
        del review
        del page
