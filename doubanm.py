import json
import re, requests
from lxml import etree


# 获取网页的源码
def get_content(url, headers):
    response = requests.get(url, headers=headers)
    return response.text


# 获取电影指定信息
def get_movie_info(text):
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
def get_movie(type, url):
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
    }
    n = 0
    # 获取api数据，并判断分页
    while True:
        text = get_content(url.format(type, n), headers=headers)
        if text == '[]':
            break
        get_movie_info(text)
        n += 20


# 主方法
def main():
    base_url = 'https://movie.douban.com/chart'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        'Referer': 'https://movie.douban.com/explore'
    }

    html_str = get_content(base_url, headers=headers)  # 分类页首页
    html = etree.HTML(html_str)
    movie_urls = html.xpath('//div[@class="types"]/span/a/@href')  # 获得每个分类的连接，但是切割type
    for url in movie_urls:
        p = re.compile('type=(.*?)&interval_id=')
        type_ = p.search(url).group(1)
        ajax_url = 'https://movie.douban.com/j/chart/top_list?type={}&interval_id=100%3A90&action=&start={}&limit=20'
        get_movie(type_, ajax_url)


if __name__ == '__main__':
    main()

