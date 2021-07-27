import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from imdb.spiders.best_movies import BestMoviesSpider # import the spider you want to debug


process = CrawlerProcess(settings=get_project_settings())
process.crawl(BestMoviesSpider)
process.start()