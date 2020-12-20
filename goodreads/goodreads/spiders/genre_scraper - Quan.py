# -*- coding: utf-8 -*-
"""
@author: quan.dh176850
"""

import scrapy
import pandas as pd
import re
from itertools import cycle


class Genre(scrapy.Spider):
    name = "genre_q"
    
    bookdb = pd.read_csv("actual_data.csv")
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
        num_people = 0
        for res in response.xpath('//div[@class="shelfStat"]'):
            genre = res.xpath('div/a/text()').get()
            people = res.xpath('div[@class="smallText"]/a/text()').get()
            num = people.split()
            people = num[0]
            if people.find(",") != -1:
                people = people.replace(",","")
            num_people = int(people)
            
            
            if genre is not None:
                if self.hasNumber(genre) == False:
                    yield {
                        'BookID' : self.nextID,
                        'Genre' : genre,
                        'NumberOfPeople' : num_people
                        }
        self.nextID = next(self.bookID)
        
        
    def hasNumber(self,string):
        return any(char.isdigit() for char in string)
    
        
