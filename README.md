# Distributed tecent_news
distributed version of tencent_news

# Changes
## settings.py
* 1. Replace Scheduler into scrapy-redis Scheduler, Dupefilter as well.Besides, some relevant rules added in settings.py.

## index_news.py
* 2. Replace the father class of IndexNewsSpider scrapy.Spider into scrapy_redis.spiders.RedisSpider.

## connection
* 1. Add redis connection for storing & getting requests.
* 2. Change the mongodb uri with remote address.
