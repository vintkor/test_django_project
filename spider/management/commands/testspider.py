from django.core.management.base import BaseCommand, CommandError
from bs4 import BeautifulSoup
import urllib.request
import csv
from catalog.models import CatalogProduct, CatalogCategory, CatalogCurrency
from decimal import Decimal


class Command(BaseCommand):
    help = 'test django command - testspider'
    line = '+' * 100
    url = 'http://imsd.com.ua/catalog/otdelochnye-materialy/stroitelnye_smesi/?PAGEN_1='

    @staticmethod
    def get_html(url):
        return urllib.request.urlopen(url)

    @staticmethod
    def save(items):
        category = CatalogCategory.objects.get(id=6)
        currency = CatalogCurrency.objects.get(id=1)
        for item in items:
            product = CatalogProduct()
            product.title = item['title']
            price = item['price'].replace('грн', '').replace(',', '.')
            product.price = Decimal(price)
            product.category = category
            product.currency = currency
            product.step = 1
            product.save()

    @staticmethod
    def save_in_csv(items, path):
        with open(path, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['title', 'price', 'image', 'link'])
            for product in items:
                writer.writerow([product['title'], product['price'], product['image'], product['link']])

    def handle(self, *args, **option):
        items = []

        # for page in range(1):
        html = self.get_html('http://his.ua/shop/index?order=product_created&direction=DESC&categoryId=29&pagersize=11')
        soup = BeautifulSoup(html, "html.parser")
        paginate = 11

        for item in soup.find_all('div', {'class': 'product_item'}):
            image = item.find('div', {'class': 'img'}).find('img')['src']
            title = item.find('h3', {'class': 'name'}).find('a').text
            price = item.find('h3', {'class': 'price'}).find('span').text

            link = item.find('h3', {'class': 'name'}).find('a')['href']

            items.append({
                'title': title,
                'price': price,
                'image': image
                # 'link': link
            })

        # for item in items:
        #     print('http://stirka.kh.ua/{}'.format(item['link']))
        #     single_html = self.get_html('http://stirka.kh.ua/{}'.format(item['link']))
        #     single_product = BeautifulSoup(single_html, 'html.parser')
        #     text = single_product.find('div', {'class': 'desc'})
        #     items.append({'text': text})
        #     print(items)


        self.save_in_csv(items, 'items.csv')
        # self.save(items)
        self.stdout.write(self.line)
