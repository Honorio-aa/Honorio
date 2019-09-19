
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
from honorio.items import HonorioItem


class HonorioSpider(CrawlSpider):
    name = 'honorio'
    item_count=0
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/page/1/']


    rules = {
            # Para cada item
            Rule(LinkExtractor(allow = (), restrict_xpaths = ('//li[@class="next"]/a/text( )'))),
            Rule(LinkExtractor(allow =(), restrict_xpaths = ('//div[@class="quote"]/span/a')),
                callback = 'parse_item', follow = False)
        }

    def parse_item(self, response):
        self.logger.info('Hi, this is an item page! %s', response.url)
        item = HonorioItem()
        item['author'] = response.xpath('//div/h3[@class="author-title"]/text()').extract()
        item['description'] = response.xpath('//div[@class="author-description"]/text()').extract()
        #item['description'] = response.xpath('//td[@id="item_description"]/text()').get()
        self.item_count += 1
        if self.item_count > 5:
            raise CloseSpider('item_exceeded')
        yield item
