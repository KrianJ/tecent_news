import requests
from scrapy.http.response.html import HtmlResponse
import re
import json


class ProxyMiddleware:
    __doc__ = """为整个爬虫项目获取随机代理"""

    @classmethod
    def get_proxy(self):
        """从代理池获取随机代理"""
        proxypool_url = 'http://127.0.0.1:5555/random'
        return requests.get(proxypool_url).text.strip()

    def process_request(self, request, spider):
        request.meta['http_proxy'] = self.get_proxy()
        print(request.meta['http_proxy'])

