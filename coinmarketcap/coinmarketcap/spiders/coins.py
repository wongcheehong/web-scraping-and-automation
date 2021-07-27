import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class CoinsSpider(CrawlSpider):
    name = 'coins'
    allowed_domains = ['coinmarketcap.com']
    start_urls = ['https://coinmarketcap.com']

    rules = (
        Rule(LinkExtractor(
            restrict_xpaths="//table/tbody/tr/td[3]//a[@class='cmc-link']"), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        yield {
            'name': response.xpath("(//h2/text())[1]").get(),
            'rank': response.xpath("//div[contains(@class, 'namePillPrimary')]/text()").get(),
            'price(USD)': response.xpath("//div[starts-with(@class, 'priceValue')]/text()").get(),
        }
