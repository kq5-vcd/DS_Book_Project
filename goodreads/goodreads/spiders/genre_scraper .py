# -*- coding: utf-8 -*-
"""
@author: quan.dh176850
"""
import os
import scrapy
import pandas as pd
from itertools import cycle

file_name = "500001-600000"

class Genre(scrapy.Spider):
    name = "genre"
    
    bookdb = pd.read_csv("books_"+file_name+".csv")
    bookdb = bookdb[bookdb.GenreLink.notnull()]
    
    try:
        f = open("genre_"+file_name+".csv","r")
        if os.stat("genre_"+file_name+".csv").st_size > 0:
            genredb = pd.read_csv(file_name)
            if genredb is not None:
                link = genredb["GenreLink"]
                link = link.drop_duplicates()
                bookdb = bookdb[~bookdb.GenreLink.isin(link)]
        else:
            f.close()
            f = open("genre_"+file_name+".csv","a")
            f.write("GenreLink,Genre,NumberOfPeople\n")
    
    except IOError:
        f = open("genre_"+file_name+".csv","w+")
        f.write("GenreLink,Genre,NumberOfPeople\n")
    finally:
        f.close()

    genreLink = bookdb["GenreLink"]
    genreLink = genreLink.drop_duplicates()
    
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
    
        
