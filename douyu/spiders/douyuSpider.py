# -*- coding: utf-8 -*-
import scrapy
import json
from douyu.items import DouyuItem


class DouyuspiderSpider(scrapy.Spider):
    name = 'douyuSpider'

    allowed_domains = ['douyu.com']
    url = 'https://www.douyu.com/gapi/rkc/directory/1_8/'
    page = 1
    start_urls = [url + str(page)]

    def parse(self, response):
        data = json.loads(response.text)['data']['rl']

        for p in data:
            items = DouyuItem()
            items['name'] = p['nn']
            items['image_urls'] = p['rs1']
            items['desc'] = p['rn']
            items['uid'] = p['uid']

            yield items


        # self.page += 1

        # yield scrapy.Request(self.url + str(self.page), callback=self.parse)
