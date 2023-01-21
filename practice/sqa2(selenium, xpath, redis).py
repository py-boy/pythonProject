"""
目标网站：https://spa2.scrape.center/（电影数据网站，无反爬，数据通过 Ajax 加载，数据接口参数加密且有时间限制，适合动态页面渲染爬取或 JavaScript 逆向分析。）
目标内容：导演照片和名字
技术栈：1，selenium访问    2，xpath提取       3，redis存储
"""
# 导入需要的包
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from redis import StrictRedis, ConnectionPool
from selenium.webdriver import ChromeOptions


# url管理函数
def urls(number):
    url = f'https://spa2.scrape.center/page/{number}'

    return url


# html访问函数
def request(url):
    # 设置无头模式
    option = ChromeOptions()
    option.add_argument('--headless')
    # 初始化浏览器
    browser = webdriver.Chrome(options=option)
    # 隐式延时等待
    browser.implicitly_wait(3)
    # 传入url，建立会话
    browser.get(url)

    return browser


# html解析函数
def extract(session, url):
    results = []
    if len(url) < 40:
        # find_elements函数定位到多个符合xpath路径的css
        elements = session.find_elements(By.XPATH, '//*[@id="index"]/div[1]/div[1]/div/div/div/div[1]/a')
        # elements是list类型，所以通过遍历的方式逐一取出
        for element in elements:
            # get_attribute函数是获取对应的属性
            href = element.get_attribute('href')
            # 添加到list列表中，才可以构成返回值
            results.append(href)

        return results
    else:
        # 更多相关搜索“提取节点信息”
        src = session.find_element(By.XPATH, '//*[@id="detail"]/div[2]/div/div/div/div/div/img').get_attribute('src')
        results.append(src)
        text = session.find_element(By.XPATH, '//*[@id="detail"]/div[2]/div/div/div/div/div/p').text
        results.append(text)

        return results


# 数据存储函数
def save(n, a):
    # 搜索“连接redis”
    pool = ConnectionPool(decode_responses=True)
    redis = StrictRedis(connection_pool=pool)
    # redis命令非常多，需要搜索
    redis.set(f'result{n}', f'{a}')


# 主函数
def main():
    number = 1
    n = 1
    session = request(urls(number))
    urls1 = extract(session, '')
    for url in urls1:
        session1 = request(url)
        a = extract(session1, url)
        save(n, a)
        n = n + 1


if __name__ == '__main__':
    main()
