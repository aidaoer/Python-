#获取B站用户主页所有视频标题和链接
#参考教程：https://mp.weixin.qq.com/s/aWratg1j9RBAjIghoY66yQ
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from parsel import Selector
import time

# 初始化WebDriver
chrome_options = Options()
# chrome_options.add_argument("--headless")  # 如果你不需要看到浏览器界面，可以加上这一行
service = Service(r'C:\Users\PycharmProjects\chromedriver-win64\chromedriver.exe')#需要替换成你的本地“chromedriver.exe”安装位置
driver = webdriver.Chrome(service=service, options=chrome_options)


def get_video_info(driver):
    # 获取页面源代码
    page_source = driver.page_source
    # 使用Parsel解析HTML
    selector = Selector(text=page_source)
    # 获取视频标题和链接
    video_elements = driver.find_elements(By.XPATH, '//*[@id="submit-video-list"]/ul/li/a[2]')
    #在需要获取的元素，这里也就是视频标题上，点击右键，复制为Xpath就能把这个路径复制出来
    # 打印结果
    for element in video_elements:
        title = element.text
        link = element.get_attribute("href")
        print(f"标题: {title}, 链接: {link}")

def main():
    base_url = "https://space.bilibili.com/280793434/video?tid=0&pn="
    start_page = 1
    max_pages = 9  # 你可以设置要爬取的最大页面数

    for page_num in range(start_page, start_page + max_pages):
        url = f"{base_url}{page_num}"
        print(f"正在爬取第 {page_num} 页: {url}")
        driver.get(url)
        # 等待页面加载
        time.sleep(4)  # 你可以增加或减少这个时间，视页面加载速度而定
        get_video_info(driver)

    # 关闭浏览器
    driver.quit()

if __name__ == "__main__":
    main()
