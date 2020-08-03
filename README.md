# tecent_news
Crawl news on news.qq.com based on scrapy

# Crawling Ideas
## 1. Analysis the method of loading Index page's data, we can find it in JS files at Network Controller in explorer.
* Request urls shape like this: https://pacaio.match.qq.com/irs/rcd?...
* We can construct the request using url above to get the js data.
* Construct the start_requests with these urls, yield index_info item by the way.

## 2. Parse the response of Index Page, get urls which direct to Detail page.
* When Detail page got, yield them to scheduler, waiting for response and parse them into detail_info item

## Tips on idea-2: 
* Detail page consist of 2 kind of pages: Template page and Normal page. We need parse them respectively.
* Tempalte page named “topic(专题)“ in Index page, which only have title and intro. in detail. Besides, it lists many of related news after the intro(JS loaded).
* The normal one is normal, parse the infomation in DOM, and nothing special yet.

## 3. Local Storage
* MongoDB as often, defined in pipeline.py, activated in settings.py

## 4. IP Proxy
* Use free IP proxy pool, listened on 5555 port locally. Defined in download middleware, activated in settings.
* No cookie proxy
