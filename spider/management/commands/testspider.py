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
    def save(items, path):
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

    def handle(self, *args, **option):
        items = []

        for page in range(1, 22):
            html = self.get_html('http://imsd.com.ua/catalog/otdelochnye-materialy/stroitelnye_smesi/?PAGEN_1={}'.format(page))
            soup = BeautifulSoup(html, "html.parser")
            paginate = 22

            for item in soup.find_all('div', {'class': 'catalog-item'}):
                image = item.find('img', {'class': 'news_img'})['src']
                items.append({
                    'title': item.find('span', {'itemprop': 'name'}).text,
                    'price': item.find('span', {'class': 'catalog-item-price'}).text,
                    'image': image
                })

        self.save(items, 'items.csv')
        self.stdout.write(self.line)
