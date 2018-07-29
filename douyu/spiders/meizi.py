# -*- coding: utf-8 -*-
import scrapy
from douyu.items import DouyuItem
import hashlib

class MeiziSpider(scrapy.Spider):
    name = 'meizi'
    allowed_domains = ['mmjpg.com']
    start_urls = ['http://mmjpg.com/']

    # url = 'http://www.mmjpg.com/mm/1421/'
    page = 1

    def parse(self, response):

        images = response.xpath("//div[@class='pic']//li/a/@href").extract()

        # 由于一直点击下一页, 到最后一页会自动进入下一组, 所以只需要取第一组链接
        link = images[0]
        yield scrapy.Request(link, callback=self.detail)
        # for link in images:
        #     yield scrapy.Request(link, callback=self.detail)



    def detail(self, response):

        imagelink = response.xpath("//div[@class='content']/a/img/@src").extract()[0]
        title = response.xpath("//div[@class='article']/h2/text()").extract()[0]
        nextLink = response.xpath("//div/a[@class='ch next']/@href").extract()[0]
        items = DouyuItem()
        items['name'] = title
        items['image_urls'] = imagelink
        items['referer'] = response.url
        items['page'] = self.page
        if response.url.count('/') == 5:
            self.page +=1

        hash_md5 = hashlib.md5(title.encode('utf-8'))
        items['folder_name'] = str(self.page) + '/' + hash_md5.hexdigest()[-5:]

        yield items

        yield scrapy.Request("http://www.mmjpg.com/" + nextLink, callback=self.detail)