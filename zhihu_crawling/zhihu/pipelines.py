# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pandas as pd
from config import FileConfig
from scrapy.exceptions import DropItem

class LivePipeline(object):
    def __init__(self):
        self.data = None

    def open_spider(self, spider):
        self.f_out = open(FileConfig["name"])
        self.data = pd.DataFrame(json.loads(line) for line in self.f_out)

    def process_item(self, item, spider):
        for each in item["data"]:
            if each["conv_id"] in self.data.conv_id.values:
                DropItem("conv_id %s already exists" % each["conv_id"])
            else:
                self.f_out.writelines(json.dumps(each) + "\n")
                self.data.append(each)

    def close_spider(self, spider):
        self.f_out.close()
