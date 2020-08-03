import scrapy
from scrapy import Request
from urllib.parse import urlencode
from tecent_news.settings import PAGE, EXT
from tecent_news.items import TecentIndexItem, DetailItem
import json
import re
import requests


class IndexNewsSpider(scrapy.Spider):
    name = 'index_news'
    allowed_domains = ['news.qq.com/']
    start_urls = ['https://news.qq.com//']

    def start_requests(self):
        base_url = 'https://pacaio.match.qq.com/irs/rcd?'
        # 构造请求字符串,控制page和callback两个动态参数
        for ext in EXT:
            for i in range(1, PAGE+1):
                for j in range(10):
                    c_back = '__jp%d' % j
                    data = {
                        'cid': 137,
                        'token': 'd0f13d594edfc180f5bf6b845456f3ea',
                        'ext': ext,
                        'page': i,
                        'callback': c_back
                    }
                    url = base_url + urlencode(data)
                    yield Request(url=url, callback=self.index_parse, dont_filter=True)

    def index_parse(self, response):
        """解析返回的json数据"""
        json_string = re.findall('({.*})', response.text)[0]
        data_list = json.loads(json_string).get('data')
        if data_list:
            item = TecentIndexItem()
            # 对json中data索引逐个抽取信息
            for data in data_list:
                item['tag'] = re.findall('(ext=.+?)&', response.url)[0][4:]
                item['category_main'] = data.get('category1_chn')
                item['category_more'] = data.get('category2_chn')
                item['bimg'] = data.get('bimg')
                item['keywords'] = data.get('keywords')
                item['source'] = data.get('source')
                item['update_time'] = data.get('update_time')
                item['vurl'] = data.get('vurl')
                yield item
                # 将详情页请求加入调度器
                detail_url = data.get('vurl')
                yield Request(url=detail_url, callback=self.detail_parse, dont_filter=True)

    def detail_parse(self, response):
        """解析详情页，详情页分两种，
            第一种是专题新闻(template)：包含标题和介绍，以及相关新闻(焦点关注)
            第二种是正常新闻"""
        item = DetailItem()
        if 'template' not in response.url:
            item['type'] = 'normal'
            item['vurl'] = response.url
            item['title'] = response.xpath('//div[@class="LEFT"]/h1/text()').extract_first()
            item['text'] = ''.join(response.xpath('//div[@class="content-article"]/p[@class="one-p"]//text()').extract()).strip()
            item['pictures'] = response.xpath('//div[@class="content-article"]/p[@class="one-p"]/img[@class="content-picture"]/@src').extract()
            yield item
        else:
            item['type'] = 'template'
            item['vurl'] = response.url
            # 获取相关新闻(js文件加载的)
            id = re.findall('id=(.*)', response.url)[0]
            item['title'], item['text'], item['related_titles'], item['related_urls'] = self.getSpecialNews(id)
            yield item

    def getSpecialNews(self, id):
        """获取专题类新闻详情页所有相关新闻标题和链接"""
        # 初始化
        related_title = []
        related_url = []
        # 构造json数据的请求url
        base_url = 'https://pacaio.match.qq.com/openapi/getQQNewsSpecialListItems?id={0}&callback=getSpecialNews'
        url = base_url.format(id)
        json_string = re.findall('({.*})', requests.get(url).text)[0]

        data = json.loads(json_string).get('data')
        # 提取标题和简介
        title = data.get('origtitle')
        intro = data.get('intro')
        # 提取目标数据
        data_list = data.get('idlist')
        for sub_part in data_list:
            # 每条section包含五条新闻
            newslist = sub_part.get('newslist')
            for news in newslist:
                title = news.get('title')
                url = news.get('url')
                related_title.append(title)
                related_url.append(url)
        return title, intro, related_title, related_url








