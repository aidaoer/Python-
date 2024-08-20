#参考教程：https://cuiqingcai.com/202253.html
import requests  # 导入requests模块，用于发送HTTP请求
import logging  # 导入logging模块，用于记录日志信息

# 配置日志记录的基本设置，设置日志级别为INFO，并定义日志输出格式
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')

# 定义一个全局变量INDEX_URL，表示用于获取电影列表的API地址
INDEX_URL = 'https://spa1.scrape.center/api/movie/?limit={limit}&offset={offset}'

# 定义一个函数scrape_api，用于发送GET请求并处理响应
def scrape_api(url):
    # 记录日志，提示正在抓取的URL
    logging.info('scraping %s...', url)
    try:
        # 发送GET请求，获取响应
        response = requests.get(url)
        # 如果响应状态码为200（表示请求成功）
        if response.status_code == 200:
            # 返回响应的JSON格式内容
            return response.json()
        # 如果状态码不是200，记录错误日志
        logging.error('get invalid status code %s while scraping %s', response.status_code, url)
    # 捕获请求异常，并记录错误日志
    except requests.RequestException:
        logging.error('error occurred while scraping %s', url, exc_info=True)

# 定义一个全局变量LIMIT，表示每页要获取的电影数量
LIMIT = 10

# 定义一个函数scrape_index，用于构造索引页的URL并调用scrape_api抓取数据
def scrape_index(page):
    # 使用format方法将LIMIT和页码计算出的偏移量填入URL
    url = INDEX_URL.format(limit=LIMIT, offset=LIMIT * (page - 1))
    # 调用scrape_api函数抓取数据并返回
    return scrape_api(url)

# 定义一个全局变量DETAIL_URL，表示用于获取电影详细信息的API地址
DETAIL_URL = 'https://spa1.scrape.center/api/movie/{id}'

# 定义一个函数scrape_detail，用于构造详细页的URL并调用scrape_api抓取数据
def scrape_detail(id):
    # 使用format方法将电影ID填入URL
    url = DETAIL_URL.format(id=id)
    # 调用scrape_api函数抓取数据并返回
    return scrape_api(url)

# 定义一个全局变量TOTAL_PAGE，表示要抓取的总页数
TOTAL_PAGE = 10

# 定义main函数，作为程序的入口
def main():
    # 遍历每一页
    for page in range(1, TOTAL_PAGE + 1):
        # 获取当前页的电影列表数据
        index_data = scrape_index(page)
        # 遍历电影列表中的每一项
        for item in index_data.get('results'):
            # 获取电影的ID
            id = item.get('id')
            # 抓取电影的详细信息
            detail_data = scrape_detail(id)
            # 记录日志，显示详细信息
            logging.info('detail data %s', detail_data)

# 判断是否以主程序形式运行，如果是，则调用main函数开始执行
if __name__ == '__main__':
    main()
