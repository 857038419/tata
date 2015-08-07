# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from doubanmovie.items import DoubanmovieItem


class MvspiderSpider(CrawlSpider):
    name = 'mvSpider'
    allowed_domains = ['movie.douban.com']
    start_urls = ['http://movie.douban.com/top250']

    rules = (
        #Rule(LinkExtractor(allow=(r'http://movie.douban.com/top250\?start=\d+.*'))),
        Rule(LinkExtractor(allow=(r'http://movie.douban.com/top250\?filter=&start=100&type=.*'))),
        
        Rule(LinkExtractor(allow=(r'http://movie.douban.com/subject/\d{6}4')),callback='parse_item'),
    )

    def parse_item(self, response):
        sel = response
        item = DoubanmovieItem()
        item['name']=sel.xpath('//*[@id="content"]/h1/span[1]/text()').extract()
        item['year']=sel.xpath('//*[@id="content"]/h1/span[2]/text()').re(r'\((\d+)\)')
        item['score']=sel.xpath('//*[@id="interest_sectl"]/div/p[1]/strong/text()').extract()
        item['director']=sel.xpath('//*[@id="info"]/span[1]/span[2]/a/text()').extract()
        item['classification']= sel.xpath('//span[@property="v:genre"]/text()').extract()
        item['actor']= sel.xpath('////*[@id="info"]/span[3]/span[2]/a/text()').extract()

        return item

# if too much  to use range  should   start items = [] for   end items.append(item)
