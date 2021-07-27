# -*- coding: utf-8 -*-
import scrapy


class GdpDebtSpider(scrapy.Spider):
    name = 'gdp_debt'
    allowed_domains = ['worldpopulationreview.com/countries/countries-by-national-debt']
    start_urls = ['https://worldpopulationreview.com/countries/countries-by-national-debt']

    def parse(self, response):
        rows = response.xpath("//tr")
        for row in rows:
            name = row.xpath(".//td[1]/a/text()").get()
            gdp_debt = row.xpath("./td[2]/text()").get()
            yield {
                'country_name': name,
                'gdp_debt': gdp_debt
            }
