# -*- coding: utf-8 -*-
import scrapy
import os
import time
import json
from zhihu.config import UsersConfig
from zhihu.items import LiveItem

class LiveSpider(scrapy.Spider):
    name = 'zhihu_live'
    domain = 'https://www.zhihu.com'
    login_url = 'https://www.zhihu.com/login/email'
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Connection": "keep-alive",
        "Host": "www.zhihu.com",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }


    def __init__(self, url = None):
        self.user_url = "https://www.zhihu.com"

    # def start_requests(self):
    #     self.request_zhihu()
    #     yield scrapy.Request(
    #         url = self.domain,
    #         headers = self.headers,
    #         meta = {
    #             'proxy': UsersConfig['proxy'],
    #             'cookiejar': 1
    #         },
    #         callback = self.request_captcha
    #     )

    # def request_captcha(self, response):
    #     # 获取_xsrf值
    #     _xsrf = response.css('input[name="_xsrf"]::attr(value)').extract()[0]
    #     # 获取验证码地址
    #     captcha_url = 'http://www.zhihu.com/captcha.gif?r=' + str(time.time() * 1000)
    #     # 准备下载验证码
    #     yield scrapy.Request(
    #         url = captcha_url,
    #         headers = self.headers,
    #         meta = {
    #             'proxy': UsersConfig['proxy'],
    #             'cookiejar': response.meta['cookiejar'],
    #             '_xsrf': _xsrf,
    #             'remember_me': 'true',
    #         },
    #         callback = self.download_captcha
    #         # callback = self.request_zhihu
    #     )

    # def download_captcha(self, response):
    #     # 下载验证码
    #     with open('captcha.gif', 'wb') as fp:
    #         fp.write(response.body)
    #     # 用软件打开验证码图片
    #     os.system('start captcha.gif')
    #     # 输入验证码
    #     print 'Please enter captcha: '
    #     captcha = raw_input()

    #     yield scrapy.FormRequest(
    #         url = self.login_url,
    #         headers = self.headers,
    #         formdata = {
    #             'email': UsersConfig['email'],
    #             'password': UsersConfig['password'],
    #             '_xsrf': response.meta['_xsrf'],
    #             'remember_me': 'true',
    #             'captcha': captcha
    #         },
    #         meta = {
    #             'proxy': UsersConfig['proxy'],
    #             'cookiejar': response.meta['cookiejar']
    #         },
    #        callback = self.request_zhihu
    #    )

    def start_requests(self):

        currentUrl = "https://api.zhihu.com/lives/hot/monthly"

        self.headers["Host"] = "api.zhihu.com"
        self.headers["authorization"] = "oauth 8274ffb553d511e6a7fdacbc328e205d"
        self.headers["x-api-version"] = "3.0.55"

        yield scrapy.Request(
            url = currentUrl,
            headers = self.headers,
            meta = {
                'proxy': UsersConfig['proxy'],
                # 'cookiejar': response.meta['cookiejar'],
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
            yield LiveItem(data=json_results["data"])

        if json_results["paging"]["is_end"] == False:
            self.nextPage = json_results["paging"]["next"]

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

            # nothing special, relay use only
            yield scrapy.Request(
                url= json_results["paging"]["next"],
                headers= relay_headers,
                meta = {
                    'proxy': UsersConfig['proxy'],
                    # 'cookiejar': response.meta['cookiejar'],
                    'from': {
                        'sign': 'else',
                        'data': {}
                    }
                },
                callback = self.monthly_live_relay,
                dont_filter = True
            )

            yield scrapy.Request(
                url=self.nextPage,
                headers=self.headers,
                meta = {
                    'proxy': UsersConfig['proxy'],
                    # 'cookiejar': response.meta['cookiejar'],
                    'from': {
                        'sign': 'else',
                        'data': {}
                    }
                },
                callback = self.monthly_live,
                dont_filter = True
            )

    def monthly_live_relay(self, response):
        # do nothing
        pass

