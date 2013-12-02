# -*- coding: utf-8 -*-
'''
Created on 30-11-2013

@author: Krzysztof Langner
'''
from opinie.items import ReviewItem
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders.crawl import Rule, CrawlSpider
from scrapy.http.request import Request
from scrapy.spider import BaseSpider
from scrapy import log
import json
import re


class OpineoSpider(CrawlSpider):
    name = "opineo"
    allowed_domains = ["ceneo.pl"]
    start_urls = ["http://www.ceneo.pl"]
    rules = (
        Rule(SgmlLinkExtractor(allow=('/produkt/')), callback='parse_product'),
        Rule(SgmlLinkExtractor(allow=())),
    )
    product_url = 'http://www.bonprix.pl/produkt'
    counter = 1
    
    def parse_product(self, response):
#        log.msg(response.url, level=log.INFO)
        m = re.search('(?<=productId:)\d+', response.body)
        if m:
            productId = m.group(0)
            return Request(url=self.product_url + "/ajax/sortByDate?productId=" + productId,
                       callback=self.parse_json)
        return []
    
    def parse_json(self, response):
        reviews = json.loads(response.body_as_unicode())
        log.msg("%d. Found %d reviews" % (self.counter, len(reviews)), level=log.INFO)
        self.counter += 1
        items = []
        for review in reviews:
            item = ReviewItem()
            item['id'] = "%s/%s#%s" % (self.product_url, review['productId'], review['id'])
            item['text'] = review['opinion']
            item['score'] = review['rating']
            item['useful'] = review['useful']
            item['notUseful'] = review['notUseful']
            items.append(item)
        return items    
    
    
class OpineoProductSpider(BaseSpider):
    name = "opineotest"
    allowed_domains = ["opineo.pl"]
    start_urls = ["http://www.opineo.pl/opinie/scandinavianbaby-pl"]
    
    def parse(self, response):
        self.dump(response.body)
        items = []
#        for review in reviews:
#            item = ReviewItem()
#            item['id'] = "%s/%s#%s" % (self.product_url, review['productId'], review['id'])
#            item['text'] = review['opinion']
#            item['score'] = review['rating']
#            item['useful'] = review['useful']
#            item['notUseful'] = review['notUseful']
#            items.append(item)
        return items    
    
    def dump(self, text):
        f = open('output/opineo.html', 'w')
        f.write(text)
        f.close()