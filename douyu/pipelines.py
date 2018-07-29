# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline
import json
from scrapy.exceptions import DropItem



class ImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        image_url = item["image_urls"]

        yield scrapy.Request(image_url,headers={'Referer':item['referer']},meta={'item':item})

    def file_path(self, request, response=None, info=None):

        item = request.meta['item']  # 通过上面的meta传递过来item
        filename = '/' + item['folder_name'] + '.jpg'
        return filename


    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item




class DouyuPipeline(object):

    def __init__(self):
        self.filename = open("douyu.json", "w")
        # self.data = []

    def process_item(self, item, spider):
        text = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.filename.write(text.encode("utf-8"))
        return item

    # def process_item(self, item, spider):
    #     self.data.append(dict(item))
    #     return item

    def close_spider(self, spider):
        # array = json.dumps(self.data, ensure_ascii=False)
        # with self.filename as f:
        #     f.write(array.encode('utf-8'))
        self.filename.close()
