from extrac_links import NetSpider
from collect_web_content import WebContentCollector


def main():
    spider = NetSpider()
    spider.BFS()
    spider.write_links_to_file()
    print('=' * 50 + '\n需要爬取的所有网页url整理结束\n' + '=' * 50 + '\n')
    print(spider.except_cnt)
    collector = WebContentCollector()
    collector.collect_obtained_url_content()
    print('=' * 50 + '\n网页内容爬取结束\n' + '=' * 50 + '\n')


if __name__ == '__main__':
    main()
