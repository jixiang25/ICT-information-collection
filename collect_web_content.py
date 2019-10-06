import requests
import json
from bs4 import BeautifulSoup


class WebContentCollector(object):
    def __init__(self):
        pass

    def url_collect(self, url):
        ret_text = {
            'title': '',
            'url': '',
            'paragraph': []
        }
        ret_text['url'] = url
        r = requests.get(url)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, features='lxml')
        ret_text['title'] = soup.title.text
        raw_content = soup.find_all('td', {'class': 'font04'})[0]
        paragraphs = raw_content.find_all(['p', 'div', 'font', 'br'])
        for para in paragraphs:
            new_paragraph = para.text.strip()
            if len(new_paragraph) > 0:
                ret_text['paragraph'].append(new_paragraph)
        return ret_text

    def collect_obtained_url_content(self, except_dir='./collect_except_url_dir.txt',
                                     data_dir='./data.txt', url_dir='./url.txt'):
        data_list, url_list, except_list = list(), list(), list()
        with open(url_dir) as f:
            for line in f:
                url_list.append(line.strip())
        for url in url_list:
            try:
                single_url_result = self.url_collect(url)
                data_list.append(single_url_result)
                print('finish ' + url + ' successfully!')
            except:
                except_list.append(url)
                print('error occurs in ' + url)
        with open(data_dir, 'w', encoding='utf-8') as f:
            for data in data_list:
                f.write(json.dumps(data, ensure_ascii=False) + '\n')
        with open(except_dir, 'w') as f:
            for except_url in except_list:
                f.write(except_url + '\n')


def main():
    collector = WebContentCollector()
    collector.collect_obtained_url_content()


if __name__ == '__main__':
    main()
