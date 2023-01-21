"""
目标网站：https://ssr2.scrape.center/（电影数据网站，无反爬，无 HTTPS 证书，适合用作 HTTPS 证书验证。）
目标内容：电影名字，评分，类别，国家，上映时间
技术栈：1,requests访问        2,XPath提取       3,JSON文本存储
"""


# 导入需要的包
import requests
from lxml import etree
import json


# 获取网页源码函数
def request(url):
    # 可以使用verify参数控制是否验证证书,如果将此参数设置为False那么在请求时就不会再验证证书是否有效。如果不设置verify参数其默认值是Ture,会自动验证.
    html = requests.get(url, verify=False)
    return html.text


# 提取信息函数
def extract(html):
    # 先使用etree.HTML(网上爬取的HTML)让其进行解析
    xhtml = etree.HTML(html)
    # 然后再使用xpath()进行数据解析，提取需要的内容
    film_name = xhtml.xpath('//*[@id="index"]/div[1]/div[1]/div[1]/div/div/div[2]/a/h2/text()')
    score = xhtml.xpath('//*[@id="index"]/div[1]/div[1]/div[1]/div/div/div[3]/p[1]/text()')
    category = xhtml.xpath('//*[@id="index"]/div[1]/div[1]/div[1]/div/div/div[2]/div[1]/button/span/text()')
    country = xhtml.xpath('//*[@id="index"]/div[1]/div[1]/div[1]/div/div/div[2]/div[2]/span[1]/text()')
    time = xhtml.xpath('//*[@id="index"]/div[1]/div[1]/div[1]/div/div/div[2]/div[3]/span/text()')
    return film_name[0], score[0].lstrip(), category, country, time


# 保存函数
def save(film_name, score, category, country, time):
    date = [{
        '电影名称': f'{film_name}',
        '评分': f'{score}',
        '类型': f'{category}',
        '国家': f'{country}',
        '上映时间': f'{time}',
    }]
    with open('movies.json', mode='w', encoding='utf-8') as file:
        file.write(json.dumps(date, indent=2, ensure_ascii=False))
    return


# 主函数
def main():
    url = 'https://ssr2.scrape.center/'
    html = request(url)
    results = extract(html)
    print(results)
    # save(results[0], results[1], results[2], results[3], results[4])


if __name__ == '__main__':
    main()
