import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from worldmeters.spiders.countries import CountriesSpider # import the spider you want to debug


process = CrawlerProcess(settings=get_project_settings())
process.crawl(CountriesSpider)
process.start()