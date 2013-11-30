# -*- coding: utf-8 -*-
'''
Created on 30-11-2013

@author: Krzysztof Langner
'''
from scrapy.spider import BaseSpider

class DmozSpider(BaseSpider):
    name = "bonprix"
    allowed_domains = ["bonprix.pl"]
    start_urls = ["http://www.bonprix.pl"]

    def parse(self, response):
        print("Parse %s" % response.url)
