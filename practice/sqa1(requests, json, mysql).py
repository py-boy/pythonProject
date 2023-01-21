"""
目标网站：https://spa1.scrape.center/（电影数据网站，无反爬，数据通过 Ajax 加载，页面动态渲染，适合 Ajax 分析和动态页面渲染爬取。）
目标内容：电影主图，电影名字
技术栈：1，requests访问        2，json数据的提取      3，MySQL存储
"""

# 导入需要的包
import requests
import json
import pymysql


# 获取网页源码函数
def request(url):
    # 通过get方法对目标网站发起请求
    html = requests.get(url)
    # 返回json格式的信息内容
    return html.json()


# 提取信息函数
def extract(jsons):
    results = jsons.get('results')
    id = results[0].get('id')
    name = results[0].get('name')
    image = results[0].get('cover')
    return id, name, image


# 保存函数
def save(id, name, image):
    # 创建一个动态字典接收数据，在大量数据需要存储的时候使用动态数据是最优的
    data = {
        'id': f'{id}',
        'filename': f'{name}',
        'image': f'{image}'
    }

    table = 'movies'
    keys = ', '.join(data.keys())
    values = ', '.join(['%s'] * len(data))
    # 连接数据库
    db = pymysql.connect(
        host='localhost',
        user='root',
        password='Asd.1018',
        port=3306,
        db='spiders'
    )
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # 使用 execute() 方法执行 SQL，如果表存在则删除
    cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")
    # 使用预处理语句创建表
    sql1 = f'CREATE TABLE IF NOT EXISTS {table}(' \
           'id INT NOT NULL, filename VARCHAR(255) NOT NULL, image VARCHAR(255) NOT NULL, PRIMARY KEY(id) )'
    cursor.execute(sql1)

    # 插入数据SQL语句，并且预防数据重复
    sql2 = f'INSERT INTO {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE '
    update = ','.join([f"{key} = %s" for key in data])
    # INSERT INTO students(id, name, age) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE id = %s, name = %s, age = %s
    sql2 += update
    try:
        # execute方法的第二个参数元组就需要乘以2，因为有6个通配符
        if cursor.execute(sql2, tuple(data.values()) * 2):
            print('Successful')
            # 在增，删，改数据时都要用commit方法提交数据
            db.commit()
    except IOError:
        print('Failed')
        # 如果执行失败, 则调用rollback执行数据回滚，相当于什么都没有发生过
        db.rollback()

    db.close()


# 主函数
def main():
    url = 'https://spa1.scrape.center/api/movie/?limit=10&offset=0'
    jsons = request(url)
    results = extract(jsons)
    save(results[0], results[1], results[2])


if __name__ == '__main__':
    main()
