import scrapy
from scrapy.http import HtmlResponse
from pymongo.mongo_client import MongoClient


class MySpider(scrapy.Spider):
    name = 'mySpider'
    # start_urls = ['https://projects.worldbank.org/en/projects-operations/project-country?lang=en&page=&_gl=1*1qm5dga*_gcl_au*NDQ5OTIwMzkyLjE3MjU5MTAxMzI.']
    
    start_urls = ['https://books.toscrape.com/']

    # Подключаемся к MongoDB
    def __init__(self):
        # Создаем подключение к MongoDB
        password="7y3sm55QTUchFKu"
        uri = f"mongodb+srv://python-user1:{password}@cluster0.mu4c0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        self.client = MongoClient(uri)
        self.db = self.client['alex_olhovskiy_test_db']
        self.collection=self.db["SpiderBook"]
    
    def parse(self, response:HtmlResponse):
        # print("Parse",response.status,response.url)
        # links=response.xpath("//li[@class='col-sm-6 col-md-6 col-lg-3']/a/@href").getall()//
        
        next_p=response.xpath("//li[@class='next']/a/@href").get()
        if next_p:
            yield response.follow(next_p,callback=self.parse)
            
        links=response.xpath("//li[@class='col-xs-6 col-sm-4 col-md-3 col-lg-3']/article/h3/a/@href").getall()
        for link in links:
            yield response.follow(link,callback=self.vacancy_parse)
        
        
                            
    def vacancy_parse(self,response:HtmlResponse):
        # Извлечение данных
        item = {
            'title': response.xpath("//h1/text()").get(),
            'price': response.xpath("//p[@class='price_color']/text()").get(),
            'url': response.url
        }

        # Сохранение данных в MongoDB
        self.collection.insert_one(item)

        # Вывод данных на экран
        print(item)

        # Возвращаем данные для Scrapy (чтобы сохранить их в файл, если настроен фид)
        yield item
        

    # Закрытие соединения с MongoDB после завершения работы паука
    def closed(self, reason):
        print("Done")
        self.client.close()

