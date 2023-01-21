"""
目标网站：https://ssr.scrape.center/
目标内容：图片，名称，类型，地区，时长，上映时间，评分
技术栈：1，aiohttp访问        2，parsel提取      3，MongoDB存储     4，异步

"""
# 导入需要的包
import asyncio
import aiohttp
import motor.motor_asyncio
from parsel import Selector


# url管理函数
async def urls(number):
    url = f'https://ssr1.scrape.center/detail/{number}'
    # await后面只能跟协程对象、future对象、task对象
    return await request(url)


# html访问函数
async def request(url):
    # aiohttp支持的并发量非常大，设置几百万，如果不加限制会对网站造成破坏；所以通过Semaphore方法限制并发量在5
    async with asyncio.Semaphore(10):
        # 通过aiohttp.ClientSession创建一个会话
        async with aiohttp.ClientSession() as session:
            # 这一句等同于response = requests.get（url）
            async with session.get(url) as response:
                html = await response.text()
                results = extract(html)

    return results


# html解析函数
def extract(html):
    selector = Selector(text=html)
    img = selector.xpath('//*[@id="detail"]/div[1]/div/div/div[1]/div/div[1]/a/img/@src').getall()
    name = selector.xpath('//*[@id="detail"]/div[1]/div/div/div[1]/div/div[2]/a/h2/text()').getall()
    category = selector.xpath('//*[@id="detail"]/div[1]/div/div/div[1]/div/div[2]/div[1]/button/span/text()').getall()
    country = selector.xpath('//*[@id="detail"]/div[1]/div/div/div[1]/div/div[2]/div[2]/span[1]/text()').getall()
    time = selector.xpath('//*[@id="detail"]/div[1]/div/div/div[1]/div/div[2]/div[2]/span[3]/text()').getall()
    ptime = selector.xpath('//*[@id="detail"]/div[1]/div/div/div[1]/div/div[2]/div[3]/span/text()').getall()
    score = selector.xpath('//*[@id="detail"]/div[1]/div/div/div[1]/div/div[3]/p[1]/text()').getall()

    return img, name, category, country, time, ptime, score


# 数据存储函数
async def save(data, collection):
    document = {
        'img': f'{data[0]}',
        'name': f'{data[1]}',
        'category': f'{data[2]}',
        'country': f'{data[3]}',
        'time': f'{data[4]}',
        'ptime': f'{data[5]}',
        'score': f'{data[6][0].strip()}'
    }
    # 写入一条数据
    await collection.insert_one(document)

    return '全部完成'


# 主函数
async def main():
    # create_task(创建一个明确的任务，例如url)；ensure_future(协程函数)。
    tasks = [asyncio.ensure_future(urls(number)) for number in range(1, 101)]
    # asyncio.gather（）和asyncio.wait（）它们执行的效果是一样，但是结果不一样，具体需要Google搜索
    results = await asyncio.gather(*tasks)

    # 指定主机和端口，连接mongodb
    client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
    # 指定数据库
    db = client.test_datebase
    # 指定集合
    collection = db.test_collection
    # 创建异步任务
    tasks1 = [asyncio.ensure_future(save(data, collection)) for data in results]
    print(await asyncio.gather(*tasks1))


if __name__ == '__main__':
    asyncio.run(main())
