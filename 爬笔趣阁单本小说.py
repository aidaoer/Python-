#通过Python爬虫下载笔趣阁单本小说
#本代码学习教程来自：https://mp.weixin.qq.com/s/5e2_r0QXUISVp9GdDsqbzg?poc_token=HM58sGajXf6R1oLnL_FCTHZFFIcXTOygILatTG5p
#每一行代码下面的 #注释 为我对代码的理解，我也是初学，不一定对，供参考
from bs4 import BeautifulSoup
#在bs4库（BeautifulSoup库）导入beautifulSoup类，用于解析HTML和XML文档
#Beautiful Soup  官方文档：https://beautifulsoup.readthedocs.io/zh-cn/latest/
import requests
#用于发送HTTP请求获取网页内容

from tqdm import tqdm
#导入 tqdm 库中的 tqdm 类，可以在循环中显示进度

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
#模拟浏览器访问信息，一开始没加，只能爬取在本地浏览器打开过的页面（只能爬第一章和章节页），加上后可以正常访问并爬取所有页面

def get_content(target):
#定义一个爬取单章小说的函数，target为形参，需要传入一个网址
    req = requests.get(url=target, headers=headers)
    #定义变量req ，用Python模块requests的get方法，获取传入网址的HTML信息，并带上headers进行请求
    req.encoding = 'utf-8'
    #将获取的HTML信息设置为常用的‘utf-8’编码方式
    html = req.text
    # 对req执行text方法，将req对象的文本内容（即HTML文档）赋值给变量html
    bf = BeautifulSoup(html, 'lxml')
    #用BeautifulSoup模块解析html，赋值给变量bf，指定解析器为'lxml'，获取可读性更强的html代码
    texts = bf.find('div', id='chaptercontent')
    #使用Beautifulsoup类的find方法，查找第一个匹配的<div>标签，标签的id属性为'chaptercontent'的内容，即正文内容，保存在变量texts
    if texts is None:
        #如果div标签不存在或者chaptercontent不存在，texts没有被存入任何参数
        raise Exception("没有找到需要爬取的内容，错误信息：")
        # 中断当前程序，抛出一个 Exception 异常，并跳转到其他程序
    content = texts.text.strip().split('\u3000' * 2)
    #用text方法，获取变量texts的文本内容，对文本内容执行strip方法，去除文本前后的空格、换行符、制表符，
    #使用split找到制定分隔符“两个空白符\u3000”将文本分割为 列表，存储列表到变量content中
    return content
    #将获取的文本列表返回给主函数，等待下一步处理
    #print(target)
    #print(content)
    #批量爬取报错时使用的两个print，判断是否正确生成待爬取链接和是否正常爬取文本内容

if __name__ == '__main__':
#如果当前.py文件名“name”和当前代码所在文件一致（当前模块被直接运行），则执行下方代码
    server = 'https://www.bqgui.cc'
    #将带爬取网站共同部分，原始链接，赋值给变量server
    book_name = "万古仙穹.txt"
    #定义文件存储名字和格式
    target ="https://www.bqgui.cc/book/824/"
    #将章节列表页面链接赋值给变量target
    req = requests.get(url=target)
    # 定义变量req，用Python模块requests的get方法，获取章节页面的HTML信息
    req.encoding = 'utf-8'
    #将获取的章节页面HTML信息设置为常用的‘utf-8’编码方式
    html = req.text
    # 对req执行text方法，将req对象的文本内容（即HTML文档）赋值给变量html
    chapter_bs = BeautifulSoup(html, 'lxml')
    #使用BeautifulSoup函数，以lxml方式，获取章节html信息，存储到变量chapter_bs中
    chapters = chapter_bs.find('div', class_='listmain')
    #在章节chapter_bs页面中，用BeautifulSoup类的find方法，查找第一个class_='listmain'的div标签，将存储到变量chapters
    chapters = chapters.find_all('a')
    #用find_all方法，再次查找之前获取的chapters中的所有<a>标签下的内容，生成列表，更新chapters存储内容
    for chapter in tqdm(chapters):
    #遍历列表chapters中的每一个元素，用进度条模块tqdm显示当前遍历进度
        chapter_name = chapter.string
        #使用.string属性，获取 chapter的第一个标签内的文本内容，也就是章节名，存储到变量chapter_name中
        url = server + chapter.get('href')
        #使用 + 拼接原始链接server和用get方法在每一行charter中找到的“href”标签下的链接
        if 'javascript' in url:
            print(f"跳过链接: {url}")
            continue
            #示例网站中有一个加载页面，href包含javascript，无法读取，这里选择跳过，避免报错
        try:
            content = get_content(url)
            #执行上方写的get_content爬取单章函数，传入拼接后的每一章节网站，返回爬取列表形式的章节文本
            with open(book_name, 'a', encoding='utf-8') as f:
                #用with管理打开关闭文件，用open的附加模式'a'打开打开之前定义爬取小说txt文件，
                #'a'模式下，文件不存在，会被创建，文件已存在，新数据会被添加到文件末尾，不覆盖原有内容
                # 将打开的文件赋值给变量f，作为（as）f，方便后续调用
                f.write(chapter_name)
                #将在章节页面爬取的章节名写入txt文件
                f.write('\n')
                #每一行之后，输入一个换行符
                f.write('\n'.join(content))
                #使用字符串方法.join(content)，将正文 列表 content 中的所有元素连接成一个字符串，每个元素之间插入 '\n'
                f.write('\n')
                #每一章节后换行一次
        except Exception as e:
            print(f"处理 {url} 时发生错误: {e}")
        #单章无法爬取时，提示对应章节报错信息，并跳过错误，继续执行后续章节爬取
