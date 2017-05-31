# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pandas as pd
from config import FileConfig

class LivePipeline(object):
    def __init__(self):
        pass

    def open_spider(self, spider):
        self.f_out = open(FileConfig["name"], "ra")
        self.data = pd.DataFrame(json.loads(line) for line in self.f_out)

    def process_item(self, item, spider):
        for each in item["data"]:
            if not ( each["conv_id"] in self.data["conv_id"].values ):
                self.f_out.write(json.dumps(each))
                self.f_out.write("\n")

        return item

    def close_spider(self, spider):
        self.f_out.close()
