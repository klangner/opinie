# -*- coding: utf-8 -*-
'''
Created on 30-11-2013

@author: Krzysztof Langner
'''
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders.crawl import Rule, CrawlSpider
from scrapy.spider import BaseSpider


class HalensSpider(CrawlSpider):
    name = "halens"
    allowed_domains = ["halens.pl"]
    start_urls = ["http://www.halens.pl"]
    rules = (
        Rule(SgmlLinkExtractor(allow=('/produkt/')), callback='parse_product'),
        Rule(SgmlLinkExtractor(allow=())),
    )
    product_url = 'http://www.halens.pl/moda-damska-sukienki-5818/sukienka-055382'
    counter = 1
    
    def parse_product(self, response):
        items = []
        return items    
    
    
class HalensProductSpider(BaseSpider):
    name = "halenstest"
    allowed_domains = ["halens.pl"]
    start_urls = ["http://www.halens.pl/moda-damska-sukienki-5818/sukienka-055382"]
    
    def parse(self, response):
        self.dump(response.body)
        return []    
    
    def dump(self, text):
        f = open('output/halens.html', 'w')
        f.write(text)
        f.close()