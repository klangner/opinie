# -*- coding: utf-8 -*-
'''
Created on 30-11-2013

@author: Krzysztof Langner
'''
from opinie.items import ReviewItem
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders.crawl import Rule, CrawlSpider
from scrapy.http.request import Request
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
import json


class BonprixSpider(CrawlSpider):
    name = "bonprix"
    allowed_domains = ["bonprix.pl"]
    start_urls = ["http://www.bonprix.pl"]
    rules = (
        Rule(SgmlLinkExtractor(allow=())),
        Rule(SgmlLinkExtractor(allow=('/produkt/*', )), callback='parse_item')
    )
    
    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        sites = hxs.select('//ul/li')
        items = []
        for site in sites:
            item = ReviewItem()
            item['title'] = site.select('a/text()').extract()
            item['link'] = site.select('a/@href').extract()
            item['desc'] = site.select('text()').extract()
            items.append(item)
        return items
    
    
class BonprixProductSpider(BaseSpider):
    ''' http://www.bonprix.pl/produkt/ajax/sortByDate?productId=22579
        productId:28675
    '''
    name = "bptest"
    allowed_domains = ["bonprix.pl"]
    start_urls = ["http://www.bonprix.pl/produkt/bluza-904911"]
    
    def parse(self, response):
        return Request(url="http://www.bonprix.pl/produkt/ajax/sortByDate?productId=22579",
                       callback=self.parse_json)
    
    def parse_json(self, response):
        reviews = json.loads(response.body_as_unicode())
        items = []
        for review in reviews:
            item = ReviewItem()
            item['id'] = review['id']
            item['text'] = review['opinion']
            item['score'] = review['rating']
            item['useful'] = review['useful']
            item['useful'] = review['useful']
            items.append(item)
        return items    