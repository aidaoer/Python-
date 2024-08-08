#下载ok资源网一部天道电视剧所有视频 https://okzyw7.com/
#参考教程https://mp.weixin.qq.com/s/_geNA6Dwo4kx25X7trJzlg
#参考教程https://cloud.tencent.com/developer/article/1751836
#注释为个人理解，初学，理解不一定对，供参考

import os
# 导入操作系统接口模块，用于创建目录、路径操作等
import ffmpy3
# 导入 ffmpy3 模块，用于处理 FFmpeg 命令
#下载链接https://ffmpeg.org/download.html
#不要下载最上方后缀名为 .taz.xz 的文件，要下载左下方Get packages & executable files 那里对应的压缩包
# 解压到本地后，把文件路径配置到环境变量，要重启python编译器才可以使用
import requests
# 导入 requests 模块，用于发送 HTTP 请求
from bs4 import BeautifulSoup
# 从 BeautifulSoup 模块中导入 BeautifulSoup 类，用于解析 HTML 文档

headers ={
    'User-Agent': 'Mozilla/5.0 (Linux; U; Android 2.2.1; zh-cn; HTC_Wildfire_A3333 Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'
}
# 定义一个字典，用于存储 HTTP 请求头
wd = "天道"
# 定义一个字符串变量，用于存储目标搜索关键字
params = {
    'wd': wd,# 设置搜索关键字参数
    'submit': 'search', # 设置提交按钮参数
}
target = 'https://okzyw7.com/'
# 定义一个字符串变量，用于存储目标网站的 URL
url = 'https://okzyw7.com/index.php/vod/detail/id/45815.html'
# 定义一个字符串变量，用于存储视频详情页面的 URL

html = requests.get(url, params=params, headers=headers).text
#（和教程中的网站post方法不一样，我用的网站是get方法） 发送 HTTP GET 请求，并获取响应的文本内容
search_html = BeautifulSoup(html, 'lxml')
# 用 BeautifulSoup 解析响应的 HTML 内容
search_div = search_html.find_all('div', class_='link clamp1 q1')
# 查找所有包含集数信息的 div 元素
if wd not in os.listdir("./"): # 如果当前目录下没有 wd 目录，则创建该目录
     os.mkdir(wd)# 创建目录


for div in search_div:# 遍历所有找到的 div 元素
    # 提取 URL 和名称
    video_url = div.text.split("$")[1] # div.text提取div元素的文本,spilt("$"),用"$"切割成列表，[1]取列表中的第二个元素,即视频 URL，
    video_name = div.text.split("$")[0]#取第一个元素，集数

    # 打印信息
    print(f"视频名称: {video_name}")# 打印视频名称
    print(f"视频 URL: {video_url}")# 打印视频 URL

    # 指定输出文件名和扩展名
    output_file = os.path.join(wd, f"{video_name}.mp4")# 生成输出文件的路径
    try: # 尝试执行以下代码块
        # 执行下载
        ffmpy3.FFmpeg(inputs={video_url: None}, outputs={output_file: None}).run()# 使用 ffmpy3 执行 FFmpeg 命令下载视频
        print(f"正在下载：{output_file}") # 打印下载状态
    except Exception as e: # 捕获所有异常
        print(f"下载失败: {e}") # 打印异常信息

#这段代码能够成功下载和拼接成mp4文件，但是下载很慢，教程中提到的异步处理目前还没学明白


