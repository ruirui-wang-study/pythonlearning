importjson, threading


class DouBan(threading.Thread):
    def __init__(self, q=None):
        super().__init__()
        self.base_url = "https://movie.douban.com/chart"
        self.headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
            'Referer': 'https://movie.douban.com/chart'
        }
