# -*- coding: utf-8 -*-
'''
Created on 30-11-2013

@author: Krzysztof Langner
'''
from opinie.items import DmozItem
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider


class DmozSpider(BaseSpider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
       "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
       "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
       ]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        sites = hxs.select('//ul/li')
        items = []
        for site in sites:
            item = DmozItem()
            item['title'] = site.select('a/text()').extract()
            item['link'] = site.select('a/@href').extract()
            item['desc'] = site.select('text()').extract()
            items.append(item)
        return items