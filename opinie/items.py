# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class ReviewItem(Item):
    id = Field()
    text = Field()
    score = Field()
    useful = Field()
    notUseful = Field()
