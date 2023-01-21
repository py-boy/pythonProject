"""
目标网站：https://ssr3.scrape.center/（电影数据网站，无反爬，带有 HTTP Basic Authentication，适合用作 HTTP 认证案例，用户名密码均为）
目标内容：电影名字，评分，类别，国家，上映时间
技术栈：1，requests访问        2，Beautiful Soup提取      3，CSV文件存储
"""

# 导入需要的包
import csv
import requests
from bs4 import BeautifulSoup


# 获取网页源码函数
def request(url):
    # 可以使用requests库自带的身份认证功能,通过auth参数即可设置
    html = requests.get(url, auth=('admin', 'admin'))
    return html.text


# 提取信息函数
def extract(html):
    # 使用LXML解析器，只需在初始化BeautifulSoup时，把第二个参数改为lxml即可
    soup = BeautifulSoup(html, 'lxml')
    # 只需要在浏览器中复制selector，放入select（）方法中，即可对需要的信息进行匹配
    # 匹配后返回的类型是list，因此要通过索引提取，再通过get_text（）方法输出
    # strip（）方法可以去除字符串两边的特殊字符，replace（）方法可以替换字符串中的特殊字符
    film_name = soup.select(
        '#index > div:nth-child(1) > div.el-col.el-col-18.el-col-offset-3 > div:nth-child(1) > div > div > '
        'div.p-h.el-col.el-col-24.el-col-xs-9.el-col-sm-13.el-col-md-16 > a > h2')[
        0].get_text().strip()
    score = soup.select(
        '#index > div:nth-child(1) > div.el-col.el-col-18.el-col-offset-3 > div:nth-child(1) > div > div > '
        'div.el-col.el-col-24.el-col-xs-5.el-col-sm-5.el-col-md-4 > p.score.m-t-md.m-b-n-sm')[
        0].get_text().strip()
    category = soup.select(
        '#index > div:nth-child(1) > div.el-col.el-col-18.el-col-offset-3 > div:nth-child(1) > div > div > '
        'div.p-h.el-col.el-col-24.el-col-xs-9.el-col-sm-13.el-col-md-16 > div.categories')[
        0].get_text().replace('\n', '')
    country = soup.select(
        '#index > div:nth-child(1) > div.el-col.el-col-18.el-col-offset-3 > div:nth-child(1) > div > div > '
        'div.p-h.el-col.el-col-24.el-col-xs-9.el-col-sm-13.el-col-md-16 > div:nth-child(3) > span:nth-child(1)')[
        0].get_text().strip()
    time = soup.select(
        '#index > div:nth-child(1) > div.el-col.el-col-18.el-col-offset-3 > div:nth-child(1) > div > div > '
        'div.p-h.el-col.el-col-24.el-col-xs-9.el-col-sm-13.el-col-md-16 > div:nth-child(4) > span')[
        0].get_text().strip()
    return film_name, score, category, country, time


# 保存函数
def save(film_name, score, category, country, time):
    # 这里首先打开data.csv文件,然后指定打开的模式为＂（即写人）,获得文件句柄, 随后调用csv库的Writer方法初始化写人对象, 传人该句柄, 然后调用writerow方法传人每行的数据,这样便完成了写人。
    with open('data.csv', mode='a', encoding='utf-8') as file:
        # 如果想修改列与列之间的分隔符(默认是逗号), 可以传人delimiter参数
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['film_name', 'score', 'category', 'country', 'time'])
        writer.writerow([f'{film_name}', f'{score}', f'{category}', f'{country}', f'{time}'])
    return


# 主函数
def main():
    url = 'https://ssr3.scrape.center/'
    html = request(url)
    results = extract(html)
    save(results[0], results[1], results[2], results[3], results[4])


if __name__ == '__main__':
    main()
