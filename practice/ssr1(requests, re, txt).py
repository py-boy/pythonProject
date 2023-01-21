"""
目标网站：https://ssr1.scrape.center/（电影数据网站，无反爬，数据通过服务端渲染，适合基本爬虫练习）
目标内容：电影名字，评分，类别，国家，上映时间
技术栈：1，使用requests进行访问     2,使用正则提取目标内容      3，使用txt文本保存数据
"""

# 导入需要用的包
import requests
import re


# 获取网页源码函数
def request(url):
    # 通过get方法对目标网站发起请求
    html = requests.get(url)
    # 返回网站源码
    return html.text


# 提取信息函数
def extract(html):
    # 以下pattern即是提取数据的表达式，（.*?)，该部分就是目标内容，是非贪婪的表达式
    film_name_pattern = '<h2 data-v-63864230="" class="m-b-sm">(.*?)</h2>'
    score_pattern = 'class="score m-t-md m-b-n-sm">.*? (.*?)</p>'
    category_pattern = 'class="el-button category el-button--primary el-button--mini">.*?<span>(.*?)</span>'
    results_pattern = '<span data-v-7f856186="">(.*?)</span>'
    # 以下返回的结果都是tuple类型
    film_name = re.findall(film_name_pattern, html, re.S)
    score = re.findall(score_pattern, html, re.S)
    category = re.findall(category_pattern, html, re.S)
    results = re.findall(results_pattern, html, re.S)
    # 所限于正则表达式，没有部分准确提取内容，只能通过范围提取，再根据索引从tuple中提取出来
    country = results[0]
    time = results[3]
    # 返回值是一个list类型
    return film_name[0], score[0], category[0], country, time


# 保存函数
def save(film_name, score, category, country, time):
    # with as是上下文管理器，就是打开文件再相对应的操作之后会自动关闭
    # 文件的打开方式有很多种，每一种方式的作用都各不相同，具体参考搜索引擎
    with open('movies.txt', mode='a', encoding='utf-8') as file:
        file.write(f'电影名称：{film_name} \n')
        file.write(f'评分：{score} \n')
        file.write(f'类别：{category} \n')
        file.write(f'国家：{country} \n')
        file.write(f'上映时间：{time} \n')
        file.write(f'{"=" * 50}\n')

    return


# 主函数
def main():
    a = 1
    while a < 9:
        url = f'https://ssr1.scrape.center/detail/{a}'
        html = request(url)
        results = extract(html)
        save(results[0], results[1].lstrip(), results[2], results[3], results[4])
        a = a + 1


if __name__ == '__main__':
    main()
