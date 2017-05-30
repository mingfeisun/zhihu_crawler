# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from config import FileConfig

class UserPipeline(object):
    def __init__(self):
        pass

    def process_item(self, item, spider):
        with open(FileConfig["name"], FileConfig["mode_append"]) as f_out:
            f_out.writelines(json.dumps(item["data"]))

        return item
