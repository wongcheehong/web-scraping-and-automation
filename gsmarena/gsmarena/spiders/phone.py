import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class PhoneSpider(CrawlSpider):
    name = 'phone'
    allowed_domains = ['www.gsmarena.com']
    start_urls = ['https://www.gsmarena.com/results.php3?nYearMin=2021&nRamMin=8000&nIntMemMin=128000&sMakers=58,73,95,82,118,9,98,80&s5Gs=0&sOSes=2&sOSversions=2920,2910&sWLANs=7']

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//div[@class='makers']/ul/li/a"), callback='parse_item', follow=True),
    )

    # parse item function
    def parse_item(self, response):
        

    def parse_item(self, response):
        cpu = ", ".join(response.xpath("//td[@data-spec='cpu']/text()").getall())
        main_camera = ", ".join(response.xpath("//td[@data-spec='cam1modules']/text()").getall())
        charging = response.xpath("//td[@data-spec='batdescription1']/../../tr[2]/td[2]/text()").getall()
        charging = ", ".join([item.strip() for item in charging])
        yield {
            'Phone Model': response.xpath("//h1[@data-spec='modelname']/text()").get(),
            'OS': response.xpath("//td[@data-spec='os']/text()").get(),
            'CPU': cpu,
            'Internal Memory': response.xpath("//td[@data-spec='internalmemory']/text()").get(),
            'UFS': response.xpath("//td[@data-spec='memoryother']/text()").get(),
            'Main Camera Spec': main_camera,
            'Main Camera Feature': response.xpath("//td[@data-spec='cam1features']/text()").get(),
            'Main Camera Video': response.xpath("//td[@data-spec='cam1video']/text()").get(),
            'Selfie Camera Spec': response.xpath("//td[@data-spec='cam2modules']/text()").get(),
            'Selfie Camera Feature': response.xpath("//td[@data-spec='cam2features']/text()").get(),
            'Selfie Camera Video': response.xpath("//td[@data-spec='cam2video']/text()").get(),
            'Battery Type': response.xpath("//td[@data-spec='batdescription1']/text()").get(),
            'Battery Charging': charging
        }