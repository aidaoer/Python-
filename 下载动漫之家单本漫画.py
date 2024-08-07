#通过Python爬虫下载动漫之家单本漫画
#本代码学习教程来自：https://mp.weixin.qq.com/s/wyS-OP04K3Vs9arSelRlyA 和 https://www.bilibili.com/read/cv36250741/
#每一行代码下面的 #注释 为我对代码的理解，我也是初学，不一定对，供参考

import os  # 导入os模块，用于文件和目录操作
import requests  # 导入requests库，用于发送HTTP请求

# 定义HTTP请求头，伪装成浏览器访问
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/80.0.3987.163 Safari/537.36"
}


# 自定义函数，用于获取漫画的章节列表
def get_chapter_list(comic_name):
    # 获取漫画章节列表的API URL
    comic_url = "https://www.idmzj.com/api/v1/comic1/comic/detail"
    # 发送GET请求，获取漫画信息
    response = requests.get(comic_url, params={"comic_py": comic_name}, headers=headers)
    #在 requests 模块中，params 参数用于向 HTTP 请求的 URL 添加 查询字符串 参数。它可以将额外的参数以字典的形式传递给请求
    if response.status_code == 200:  # 检查请求是否成功
        comic_info = response.json()  # 解析响应的JSON数据
        comic_title = comic_info["data"]["comicInfo"]["title"]  # 提取漫画标题
        comic_id = comic_info["data"]["comicInfo"]["id"]  # 提取漫画ID
        chapters = comic_info["data"]["comicInfo"]["chapterList"][0]["data"]
        # 提取章节列表，之前是字典，[0]后面是列表，提取方式不一样，容易看混
        return comic_title, comic_id, chapters  # 返回漫画标题、ID和章节列表
    else:
        print(f"获取{comic_name}漫画信息失败")  # 请求失败时输出错误信息
        return None, None, []  # 返回空值表示获取信息失败


# 自定义函数，用于下载每个章节的图片
def download_chapter_images(comic_title, comic_id, chapter):
    # 获取漫画章节图片的API URL
    chapter_url = "https://www.idmzj.com/api/v1/comic1/chapter/detail"
    # 发送GET请求，获取章节信息
    response = requests.get(chapter_url, params={"comic_id": comic_id, "chapter_id": chapter["chapter_id"]},
                            headers=headers)
    if response.status_code == 200:  # 检查请求是否成功
        chapter_info = response.json()  # 解析响应的JSON数据
        chapter_title = chapter_info["data"]["chapterInfo"]["title"]  # 提取章节标题
        page_urls = chapter_info["data"]["chapterInfo"]["page_url"]  # 提取图片URL列表

        # 创建章节文件夹
        chapter_dir = f"./{comic_title}/{chapter_title}"
        #创建一个字符串，表示文件夹的路径。路径的格式为：当前目录（./），然后是漫画标题，接着是章节标题。
        # 例如， "./妖神记/第84话"
        os.makedirs(chapter_dir, exist_ok=True)
        #os.makedirs()：这是 Python 的 os 模块中的一个函数，用于递归地创建目录
        # 如果 chapter_dir 路径中的目录不存在，os.makedirs() 会创建这些目录。如果目录已经存在，则由于 exist_ok=True，函数不会引发异常，而是直接继续执行。

        # 遍历每个图片URL并下载
        for page_url in page_urls:
            download_image(page_url, chapter_dir)
    else:
        print(f"获取{comic_title}章节信息失败")  # 请求失败时输出错误信息


# 自定义函数，用于下载单个图片
def download_image(url, folder_path):
    # 从URL中提取图片名称
    img_name = url.split('/')[-1]
    #split('/')：这是 Python 字符串的 split() 方法。它将字符串 url 按照指定的分隔符 / 分割成多个部分，返回一个列表。
    # [-1]是一个列表索引操作，表示获取列表的最后一个元素,即图片名称和格式
    img_path = os.path.join(folder_path, img_name)  # 拼接图片保存路径
    response = requests.get(url, headers=headers)  # 发送GET请求下载图片
    if response.status_code == 200:  # 检查请求是否成功
        with open(img_path, "wb") as f:  # 以二进制写入模式打开文件
            f.write(response.content)  # 将图片内容写入文件
    else:
        print(f"下载图片{img_name}失败")  # 请求失败时输出错误信息


# 自定义函数，程序的主入口
def main():
    comic_name = "yaoshenji"  # 替换为你想要爬取的漫画名称
    comic_title, comic_id, chapters = get_chapter_list(comic_name)  # 获取漫画标题、ID和章节列表
    if comic_title:  # 如果成功获取到漫画标题
        for chapter in chapters:  # 遍历每个章节
            download_chapter_images(comic_title, comic_id, chapter)  # 下载章节的所有图片


# 检查当前脚本是否作为主程序执行
if __name__ == "__main__":
    main()  # 调用主函数
