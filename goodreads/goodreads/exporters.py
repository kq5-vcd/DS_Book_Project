# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 19:02:33 2020

@author: quan.dh176850
"""
from scrapy.exporters import CsvItemExporter


class HeadlessCsvItemExporter(CsvItemExporter):

    def __init__(self, *args, **kwargs):
        
        kwargs['include_headers_line'] = False
        super(HeadlessCsvItemExporter, self).__init__(*args, **kwargs)