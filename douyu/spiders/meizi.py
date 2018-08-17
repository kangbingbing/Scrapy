# -*- coding: utf-8 -*-
import scrapy
from douyu.items import DouyuItem
import hashlib
import re
from douyu.MysqlHelper import MysqlHelper

class MeiziSpider(scrapy.Spider):
    name = 'meizi'
    allowed_domains = ['mmjpg.com']
    start_urls = ['http://mmjpg.com/']

    # url = 'http://www.mmjpg.com/mm/1421/'

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
        page = re.findall(r"mm/(\d+)", response.url)[0]
        items['page'] = page

        hash_md5 = hashlib.md5(imagelink.encode('utf-8'))
        items['folder_name'] = str(page) + '/' + hash_md5.hexdigest()[-5:]


        sql = "SELECT * FROM mm_mmitem WHERE image_url = %s"
        helper = MysqlHelper()
        result = helper.fetchall(sql,[imagelink])
        self.log(result)


        # 先检查类型
        sql1 = "SELECT * FROM mm_mmtype WHERE id = %s"
        helper1 = MysqlHelper()
        result1 = helper1.fetchall(sql1,[int(page)])
        if len(result1) == 0:
            sql2 = 'insert into mm_mmtype(title,name,pic_url,pic_path,id) values(%s,%s,%s,%s,%s)'
            helper2 = MysqlHelper()
            filename = '/' + items['folder_name'] + '.jpg'
            helper2.insert(sql2, [items['name'],'', items['image_urls'], filename,items['page']])


        if len(result) == 0:
            # 如果没有查询到之前的, 就继续, 否则就停止
            yield items
            yield scrapy.Request("http://www.mmjpg.com/" + nextLink, callback=self.detail)


