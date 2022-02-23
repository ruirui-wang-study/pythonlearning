import json, threading
import re, requests
from lxml import etree
from queue import Queue


class DouBan(threading.Thread):
    def __init__(self, q=None):
        super().__init__()
        self.base_url = 'https://movie.douban.com/chart'
        self.headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
            'Referer': 'https://movie.douban.com/explore'
        }
        self.q = q
        self.ajax_url = 'https://movie.douban.com/j/chart/top_list?type={}&interval_id=100%3A90&action=&start={}&limit=20'

    # 获取网页的源码
    def get_content(self, url, headers):
        response = requests.get(url, headers=headers)
        return response.text

    # 获取电影指定信息
    def get_movie_info(self, text):
        text = json.loads(text)
        item = {}
        for data in text:
            score = data['score']
            image = data['cover_url']
            title = data['title']
            actors = data['actors']
            detail_url = data['url']
            vote_count = data['vote_count']
            types = data['types']
            item['评分'] = score
            item['图片'] = image
            item['电影名'] = title
            item['演员'] = actors
            item['详情页链接'] = detail_url
            item['评价数'] = vote_count
            item['电影类别'] = types
            print(item)

    # 获取电影api数据的
    def get_movie(self):
        headers = {
            'X-Requested-With':
            'XMLHttpRequest',
            'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        }

        # 获取api数据，并判断分页
        while True:
            if self.q.empty():
                break
            n = 0
            while True:
                text = self.get_content(self.ajax_url.format(self.q.get(), n),
                                        headers=headers)
                if text == '[]':
                    break
                self.get_movie_info(text)
                n += 20

    # 获取所有类型的type——id
    def get_types(self):
        html_str = self.get_content(self.base_url,
                                    headers=self.headers)  # 分类页首页
        html = etree.HTML(html_str)
        types = html.xpath(
            '//div[@class="types"]/span/a/@href')  # 获得每个分类的连接，但是切割type
        # print(types)
        type_list = []
        for i in types:
            p = re.compile('type=(.*?)&interval_id=')  # 筛选id，拼接到api接口的路由
            type = p.search(i).group(1)
            type_list.append(type)
        return type_list

    def run(self):
        self.get_movie()


if __name__ == '__main__':
    # 创建消息队列
    q = Queue()
    # 将任务队列初始化，将我们的type放到消息队列中
    t = DouBan()
    types = t.get_types()
    for tp in types:
        q.put(tp[0])
    # 创建一个列表，列表的数量就是开启线程的树木
    crawl_list = [1, 2, 3, 4]
    for crawl in crawl_list:
        # 实例化对象
        movie = DouBan(q=q)
        movie.start()
