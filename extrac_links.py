import requests
import queue
from time import sleep
from bs4 import BeautifulSoup


class NetSpider(object):
    def __init__(self):
        self.links = list()
        self.links_mp = dict()
        self.pdf_links = list()
        self.pdf_mp = dict()
        self.except_cnt = 0
        self.ALLOW_URL_PREFIX = [
            'http://www.ict.cas.cn',
            'http://www.ict.ac.cn',
        ]
        self.FORBIDDEN_URL_SUFFIX = [
            '.jpg',
            '.png',
            '.gif',
        ]

    def __match_pattern(self, text, pattern, type):
        pattern_len = len(pattern)
        text_len = len(text)
        if pattern_len > text_len:
            return False
        # print(text[:pattern_len], pattern)
        if type == 'prefix':
            return text[:pattern_len] == pattern
        else:
            return text[text_len - pattern_len: text_len] == pattern

    def __url_spread(self, url, Q):
        r = requests.get(url)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, features='lxml')
        a_links = soup.find_all('a')
        # 当前url所在的相对路径,假设http://www.ict.ac.cn/jssgk/,相对路径就是http://www.ict.ac.cn/jssgk/
        # 但是http://www.ict.ac.cn/jssgk/20191006.html的相对路径是http://www.ict.ac.cn/jssgk/
        url_prefix = url
        if self.__match_pattern('.html', url, type='suffix'):
            pos = -1
            for idx in range(url_prefix):
                if url_prefix[idx] == '/':
                    pos = idx
            url_prefix = url_prefix[:pos]
        for a_link_label in a_links:
            if a_link_label.get('href') is not None:
                a_link = a_link_label['href']
            else:
                continue
            a_link = ''.join(a_link.split())
            # 前缀是./先做替换
            if self.__match_pattern(a_link, './', type='prefix'):
                if url[-1] == '/':
                    a_link = url_prefix + a_link[2:]
                else:
                    a_link = url_prefix + '/' + a_link[2:]
            # 出现就不再访问，并且这里要排除等价域名
            if self.links_mp.get(a_link) is not None:
                continue
            if self.links_mp.get(a_link.replace('http://www.ict.cas.cn', 'http://www.ict.ac.cn')) is not None:
                continue
            if self.links_mp.get(a_link.replace('http://www.ict.ac.cn', 'http://www.ict.cas.cn')) is not None:
                continue
            # 前缀检查
            pass_prefix_check = False
            for prefix in self.ALLOW_URL_PREFIX:
                if self.__match_pattern(a_link, prefix, type='prefix'):
                    pass_prefix_check = True
                    break
            if not pass_prefix_check:
                continue
            # 后缀检查
            pass_suffix_check = True
            for suffix in self.FORBIDDEN_URL_SUFFIX:
                if self.__match_pattern(a_link, suffix, type='suffix'):
                    pass_suffix_check = False
                    break
            if not pass_suffix_check:
                continue
            # 检查是不是pdf
            if self.__match_pattern(a_link, 'pdf', type='suffix'):
                if self.pdf_mp.get(a_link) is None:
                    self.pdf_links.append(a_link)
                    self.pdf_mp[a_link] = 1
                continue
            # 入队并标记
            Q.put(a_link)
            self.links.append(a_link)
            self.links_mp[a_link] = 1

    def BFS(self):
        Q = queue.Queue()
        index_url = 'http://www.ict.ac.cn'
        Q.put(index_url)
        self.links.append(index_url)
        self.links_mp[index_url] = 1
        cnt = 1
        while not Q.empty():
            url = Q.get()
            print(url, cnt)
            self.__url_spread(url, Q)
            cnt += 1

    def write_links_to_file(self, file_dir='./url.txt', pdf_file_dir='./pdf_url.txt'):
        with open(file_dir, 'w') as f:
            for a_link in self.links:
                f.write(a_link + '\n')
        with open(pdf_file_dir, 'w') as f:
            for a_link in self.pdf_links:
                f.write(a_link + '\n')


def main():
    spider = NetSpider()
    spider.BFS()
    spider.write_links_to_file()
    print(spider.except_cnt)


if __name__ == '__main__':
    main()
