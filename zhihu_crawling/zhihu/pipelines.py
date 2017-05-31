# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import os.path
import pandas as pd
from config import FileConfig
from scrapy.exceptions import DropItem

class LivePipeline(object):
    def __init__(self):
        self.live_data = None
        self.comment_folder = "comments/"

    def open_spider(self, spider):
        self.live_outfile = open(FileConfig["name"], "r")
        self.live_data = pd.DataFrame(json.loads(line) for line in self.live_outfile)
        self.live_outfile.close()

        self.live_outfile = open(FileConfig["name"], "a")

    def process_item(self, item, spider):
        if item["type"] == "live":
            self.process_live_data(item)

        if item["type"] == "comment":
            self.process_comment_data(item)

    def close_spider(self, spider):
        self.live_outfile.close()

    def process_live_data(self, item):
        for each in item["data"]:
            if each["id"] in self.live_data.id.values:
                DropItem("live id %s already exists" % each["id"])
            else:
                self.live_outfile.writelines(json.dumps(each) + "\n")
                self.live_data.append(each)

    def process_comment_data(self, item):
        if os.path.exists( self.comment_folder + item["id"]):
            comment_outfile = open( self.comment_folder + item["id"])
            comment_data = pd.DataFrame(json.loads(line) for line in comment_outfile)
            for each in item["data"]:
                if each["id"] in comment_data.id.values:
                    DropItem("comment id %s already exists!" % each["id"])
                else:
                    comment_outfile.writelines(json.dumps(each) + "\n")
                    comment_data.append(each)
        else:
            comment_outfile = open( self.comment_folder + item["id"], "w")
            for each in item["data"]:
                comment_outfile.writelines(json.dumps(each) + "\n")

