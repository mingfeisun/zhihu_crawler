# -*- coding: utf-8 -*-
import scrapy
import json
from zhihu.config import UsersConfig
from zhihu.items import LiveItem
from zhihu.items import CommentItem

class LiveSpider(scrapy.Spider):
    name = "zhihu_live"

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Connection": "keep-alive",
        "Host": "api.zhihu.com",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "authorization": "oauth 8274ffb553d511e6a7fdacbc328e205d",
        "x-api-version": "3.0.55"
    }

    relay_headers = {
        "Accept" : "*/*",
        "Accept-Encoding" : "gzip, deflate, sdch, br",
        "Accept-Language" : "en,zh-CN;q=0.8,zh;q=0.6,zh-TW;q=0.4",
        "Access-Control-Request-Headers" : "authorization,x-api-version",
        "Access-Control-Request-Method": "GET",
        "Connection" : "keep-alive",
        "Host":"api.zhihu.com",
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    def __init__(self):
        pass

    def start_requests(self):
        currentUrl = "https://api.zhihu.com/lives/hot/monthly"
        yield scrapy.Request(
            url= currentUrl,
            headers= self.headers,
            meta = {
                'proxy': UsersConfig['proxy'],
                'from': {
                    'sign': 'else',
                    'data': {}
                }
            },
            callback = self.monthly_live,
            dont_filter = True
        )

    def monthly_live(self, response):
        json_results = json.loads(response.body)

        if json_results["data"] is not None:
            yield LiveItem(data=json_results["data"], type="live")

            for each in json_results["data"]:
                nextPage = "https://www.zhihu.com/lives/" + each["id"] + "/reviews"
                yield scrapy.Request(
                    url= nextPage,
                    headers= self.relay_headers,
                    meta = {
                        'proxy': UsersConfig['proxy'],
                        'from': {
                            'sign': 'else',
                            'data': {}
                        }
                    },
                    callback = None,
                    dont_filter = True
                )

                yield scrapy.Request(
                    url= nextPage,
                    headers= self.headers,
                    meta = {
                        'id': each["id"],
                        'proxy': UsersConfig['proxy'],
                        'from': {
                            'sign': 'else',
                            'data': {}
                        }
                    },
                    callback = self.live_comment,
                    dont_filter = True
                )

        if json_results["paging"]["is_end"] == False:
            nextPage = json_results["paging"]["next"]

            yield scrapy.Request(
                url= nextPage,
                headers= self.relay_headers,
                meta = {
                    'proxy': UsersConfig['proxy'],
                    'from': {
                        'sign': 'else',
                        'data': {}
                    }
                },
                callback = None,
                dont_filter = True
            )

            yield scrapy.Request(
                url= nextPage,
                headers= self.headers,
                meta = {
                    'proxy': UsersConfig['proxy'],
                    'from': {
                        'sign': 'else',
                        'data': {}
                    }
                },
                callback = self.monthly_live,
                dont_filter = True
            )


    def live_comment(self, response):
        json_results = json.loads(response.body)
        # print "######################################"
        # print response.meta["id"]
        # print "######################################"
        yield CommentItem(data=json_results["data"], type="comment", id=response.meta["id"])

