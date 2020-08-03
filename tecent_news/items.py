from scrapy import Item, Field


class TecentIndexItem(Item):
    collection = 'index_info'
    category_main = Field()         # 新闻主体类
    category_more = Field()         # 新闻细分类
    bimg = Field()                  # 背景图
    keywords = Field()              # 新闻关键词
    source = Field()                # 来源
    update_time = Field()           # 发布时间
    vurl = Field()                  # 网页版链接
    tag = Field()                   # 新闻栏目


class DetailItem(Item):
    collection = 'detail_info'
    type = Field()                  # 详情页种类
    vurl = Field()                  # 新闻链接
    title = Field()                 # 新闻标题
    text = Field()                  # 正文
    pictures = Field()              # 新闻配图
    related_titles = Field()        # 专题类新闻乡相关标题
    related_urls = Field()          # 专题类新闻相关新闻
