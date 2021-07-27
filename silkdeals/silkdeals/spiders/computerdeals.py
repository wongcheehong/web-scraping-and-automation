import scrapy
from scrapy_selenium import SeleniumRequest


class ComputerdealsSpider(scrapy.Spider):
    name = 'computerdeals'

    def start_requests(self):
        yield SeleniumRequest(
            url='https://slickdeals.net/computer-deals/',
            wait_time=3,
            callback=self.parse
        )

    def parse(self, response):
        products = response.xpath("//ul[@class='dealTiles categoryGridDeals']/li")
        for product in products:
            yield {
                'name': product.xpath(".//a[contains(@class, 'itemTitle')]/text()").get(),
                'url': product.xpath(".//a[contains(@class, 'itemTitle')]/@href").get(),
                'store_name': product.xpath("normalize-space((.//button[contains(@class, 'itemStore')] | .//a[contains(@class, 'itemStore')])/text())").get(),
                'price': product.xpath("normalize-space(.//div[@class='itemPrice  wide ']/text())").get()
            }

        next_page = response.xpath("//a[@data-role='next-page']/@href").get()
        if next_page:
            absolute_url = f"https://slickdeals.net{next_page}"
            yield SeleniumRequest(
                url=absolute_url,
                wait_time=3,
                callback=self.parse
            )