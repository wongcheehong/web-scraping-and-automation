import scrapy
from scrapy_splash import SplashRequest


class QuoteSpider(scrapy.Spider):
    name = 'quote'
    allowed_domains = ['quotes.toscrape.com']

    script = '''
    function main(splash, args)
        assert(splash:go(args.url))
        assert(splash:wait(1))
        return splash:html()
    end
    '''

    def start_requests(self):
        yield SplashRequest(url="http://quotes.toscrape.com/js/", callback=self.parse, endpoint="execute", args={
            'lua_source': self.script
        })

    def parse(self, response, **kwargs):
        for quote in response.xpath("//div[@class='quote']"):
            # tags_list = quote.xpath(".//div/a/text()").getall()
            # tags = ", ".join(tags_list)
            yield {
                'quote_text': quote.xpath(".//span[1]/text()").get(),
                'author': quote.xpath(".//span[2]/small/text()").get(),
                'tags': quote.xpath(".//div/a/text()").getall()
            }

        next_page = response.xpath("//li[@class='next']/a/@href").get()
        if next_page:
            absolute_url = f"http://quotes.toscrape.com{next_page}"
            yield SplashRequest(url=absolute_url, callback=self.parse, endpoint="execute", args={
                'lua_source': self.script
            })