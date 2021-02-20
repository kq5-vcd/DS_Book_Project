# -*- coding: utf-8 -*-
"""
@author: quan.dh176850
"""

import scrapy
import pandas as pd
from itertools import cycle


class Genre(scrapy.Spider):
    name = "genre"
    
    bookdb = pd.read_csv("actual_data.csv")
    genreLink = bookdb["GenreLink"]
    
    start_urls = ["https://www.goodreads.com{}".format(link) for link in genreLink]
    
    def parse(self, response):
        
        genre = ""
        num_people = 0
        for res in response.xpath('//div[@class="shelfStat"]'):
            genre = res.xpath('div[@style="float: left; width: 100px;"]/a/text()').get()
            people = res.xpath('div[@class="smallText"]/a/text()').get()
            num = people.split()
            people = num[0]
            if people.find(",") != -1:
                people = people.replace(",","")
            num_people = int(people)
            
            
            if genre is not None:
                if self.hasNumber(genre) == False:
                    yield {
                        'GenreLink' : response.request.url[25:],
                        'Genre' : genre,
                        'NumberOfPeople' : num_people
                        }
        
        
        
    def hasNumber(self,string):
        return any(char.isdigit() for char in string)
    
        
