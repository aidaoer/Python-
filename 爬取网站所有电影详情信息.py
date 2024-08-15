#爬取示例网站所有电影详情信息，并单独存储到每个json文件
#参考教程：https://cuiqingcai.com/202224.html
import requests  # 导入 requests 库，用于发送 HTTP 请求
import logging  # 导入 logging 库，用于记录日志信息
import re  # 导入 re 库，用于使用正则表达式进行字符串匹配
from urllib.parse import urljoin  # 从 urllib.parse 模块中导入 urljoin，用于拼接 URL

import json  # 导入 json 库，用于处理 JSON 格式的数据
from os import makedirs  # 从 os 模块中导入 makedirs 函数，用于创建目录
from os.path import exists  # 从 os.path 模块中导入 exists 函数，用于检查路径是否存在

import multiprocessing  # 导入 multiprocessing 库，用于实现多进程处理

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')  # 配置日志的基本设置，设置日志等级为 INFO，指定日志的输出格式

BASE_URL = 'https://ssr1.scrape.center'  # 定义一个基础 URL，用于构建其他页面的完整 URL
TOTAL_PAGE = 10  # 定义总页数为 10

RESULTS_DIR = 'results'  # 定义存储结果的目录
exists(RESULTS_DIR) or makedirs(RESULTS_DIR)  # 如果目录不存在则创建它

def scrape_page(url):
    logging.info('正在爬取…… %s ', url)  # 记录日志，显示当前正在爬取的 URL
    try:
        response = requests.get(url)  # 发送 GET 请求获取网页内容
        if response.status_code == 200:  # 如果响应状态码为 200，表示请求成功
            return response.text  # 返回网页的文本内容
        logging.error('爬取网址 %s 的状态码： %s', url, response.status_code)  # 如果状态码不是 200，记录错误日志
    except requests.RequestException:
        logging.error('爬取网址出现错误  %s', url, exc_info=True)  # 捕获请求异常并记录错误日志，exc_info=True 会输出详细的错误堆栈信息

def scrape_index(page):
    index_url = f'{BASE_URL}/page/{page}'  # 构建索引页的 URL
    return scrape_page(index_url)  # 调用 scrape_page 函数爬取索引页

def parse_index(html):
    pattern = re.compile('<a.*?href="(.*?)".*?class="name">')  # 使用正则表达式匹配电影详情页的链接
    items = re.findall(pattern, html)  # 在 html 内容中查找所有匹配的链接
    if not items:  # 如果没有找到任何匹配项，返回空列表
        return []
    for item in items:
        detail_url = urljoin(BASE_URL, item)  # 使用 urljoin 拼接出完整的电影详情页链接
        logging.info('获取电影详情页链接 %s', detail_url)  # 记录日志，显示获取到的电影详情页链接
        yield detail_url  # 使用 yield 生成器返回电影详情页链接

def scrape_detail(url):
    return scrape_page(url)  # 调用 scrape_page 函数爬取电影详情页

def parse_detail(html):
    cover_pattern = re.compile('class="item.*?<img.*?src="(.*?)".*?class="cover">', re.S)  # 匹配电影封面的正则表达式
    name_pattern = re.compile('<h2.*?>(.*?)</h2>')  # 匹配电影名称的正则表达式
    categories_pattern = re.compile('<button.*?category.*?<span>(.*?)</span>.*?</button>', re.S)  # 匹配电影分类的正则表达式
    published_at_pattern = re.compile(r'(\d{4}-\d{2}-\d{2})\s?上映')  # 匹配上映日期的正则表达式
    drama_pattern = re.compile('<div.*?drama.*?>.*?<p.*?>(.*?)</p>', re.S)  # 匹配剧情简介的正则表达式
    score_pattern = re.compile('<p.*?score.*?>(.*?)</p>', re.S)  # 匹配电影评分的正则表达式
    cover = re.search(cover_pattern, html).group(1).strip() if re.search(cover_pattern, html) else None  # 提取封面链接
    name = re.search(name_pattern, html).group(1).strip() if re.search(name_pattern, html) else None  # 提取电影名称
    categories = re.findall(categories_pattern, html) if re.findall(categories_pattern, html) else []  # 提取电影分类
    published_at = re.search(published_at_pattern, html).group(1) if re.search(published_at_pattern, html) else None  # 提取上映日期
    drama = re.search(drama_pattern, html).group(1).strip() if re.search(drama_pattern, html) else None  # 提取剧情简介
    score = float(re.search(score_pattern, html).group(1).strip()) if re.search(score_pattern, html) else None  # 提取电影评分并转换为浮点数
    return {
        'cover': cover,
        'name': name,
        'categories': categories,
        'published_at': published_at,
        'drama': drama,
        'score': score
    }  # 返回一个包含电影信息的字典

def save_data(data):
    name = data.get('name')  # 获取电影名称
    data_path = f'{RESULTS_DIR}/{name}.json'  # 构建 JSON 文件的保存路径
    json.dump(data, open(data_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)  # 将电影信息保存为 JSON 文件

#def main():
#    for page in range(1, TOTAL_PAGE + 1):
#        index_html = scrape_index(page)
##        detail_urls = parse_index(index_html)
 #       for detail_url in detail_urls:
 #           detail_html = scrape_detail(detail_url)
  #          data = parse_detail(detail_html)
  #          logging.info('电影详情页数据 %s', data)
   #         logging.info('保存数据到json文件')
   #         save_data(data)
   #         logging.info('json格式详情数据保存成功！')

def main(page):  # 定义 main 函数处理单个页面的爬取和解析
    index_html = scrape_index(page)  # 爬取索引页
    detail_urls = parse_index(index_html)  # 解析出电影详情页链接
    for detail_url in detail_urls:  # 遍历所有详情页链接
        detail_html = scrape_detail(detail_url)  # 爬取详情页内容
        data = parse_detail(detail_html)  # 解析详情页内容
        logging.info('电影详情页数据 %s', data)  # 记录解析后的电影详情数据
        logging.info('保存数据到json文件')  # 记录即将保存数据的日志
        save_data(data)  # 保存数据到 JSON 文件
        logging.info('json格式详情数据保存成功！')  # 记录数据保存成功的日志

if __name__ == '__main__':  # 判断当前模块是否为主模块
    pool = multiprocessing.Pool()  # 创建一个进程池
    pages = range(1, TOTAL_PAGE + 1)  # 定义要爬取的页码范围
    pool.map(main, pages)  # 使用进程池的 map 函数并行执行 main 函数，传入页码作为参数
    pool.close()  # 关闭进程池，不再接受新的任务
    pool.join()  # 等待所有子进程完成任务
