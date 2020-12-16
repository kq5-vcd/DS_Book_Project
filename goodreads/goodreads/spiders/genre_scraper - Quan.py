# -*- coding: utf-8 -*-
"""
@author: quan.dh176850
"""

import scrapy
import pandas as pd
from itertools import cycle


class Genre(scrapy.Spider):
    name = "genre_q"
    
    bookdb = pd.read_csv("books_q.csv")
    bookdb = bookdb[bookdb.GenreLink.notnull()]

    genredb = pd.read_csv("genre_q.csv")
    if genredb is not None:
        bID = genredb["BookID"]
        bID = bID.drop_duplicates()
        bookdb = bookdb[~bookdb.BookID.isin(bID)]
    
    bookID = cycle(bookdb["BookID"])
    nextID = next(bookID)
    genreLink = bookdb["GenreLink"]
    
    start_urls = ["https://www.goodreads.com{}".format(link) for link in genreLink]
    
    def parse(self, response):
        genre = ""
        for res in response.xpath('//div[@class="shelfStat"]'):
            genre = res.xpath('div/a/text()').get()
            
            if genre is not None:
                if self.hasNumber(genre) == False:
                    yield {
                        'BookID' : self.nextID,
                        'Genre' : genre
                        }
        self.nextID = next(self.bookID)
        
        
    def hasNumber(self,string):
        return any(char.isdigit() for char in string)
    
        
