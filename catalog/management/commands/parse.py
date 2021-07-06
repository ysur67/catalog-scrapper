from django.core.management.base import BaseCommand, CommandError
from bs4 import BeautifulSoup
import requests
from catalog.models import Product
from decimal import Decimal


class Command(BaseCommand):
    DEFAULT_URL = "https://foxweld.ru/products/elektrosvarka/"

    def add_arguments(self, parser):
        parser.add_argument('--url', default=self.DEFAULT_URL)
    
    def handle(self, *args, **options):
        url = options.get('url')
        request = requests.get(url)
        soup = BeautifulSoup(request.text)
        items = soup.find_all('li', {'class': 'item'})
        for item in items:
            product_for_import = self.get_product_dict(item)
            self._import_product(product_for_import)
            
    def get_product_dict(self, product):
        """Получить словарь модели продукта, готовый к импорту.

        Args:
            product: Карточка товара с html строки

        Returns:
            dict: Продукт
        """
        id_ = self._get_id(product)
        title_block = product.find("div", {'class': 'name'})
        props_block = product.find("div", {"class": "props"})
        product_props = self._get_props(props_block)
        price_block = product.find("span", {"class", "price-val"})
        price_value = price_block.find("b")
        
        product_title = self._clear(title_block.text)
        product_price = self._clear(price_value.text)
        for key in product_props:
            product_props[key] = self._clear(product_props[key])

        print(f"{product_title} price: {product_price} props: {product_props}")
            
        result = {}
        result['id'] = id_
        result['title'] = product_title
        result['price'] = self._get_price(product_price)
        result['code'] = product_props['Артикул:']
        result['series'] = product_props['Серия:']
        
        return result     
        
    def _get_id(self, product):
        id_ = product.attrs.get("data-id", None)
        if not id_:
            # Если блок не содержит идентификатора - вернуть новый ид из бд
            return Product.get_next()

        try:
            result = int(id_)
        except ValueError:
            result = Product.get_next()
        
        return result
        
    def _get_props(self, props_block):
        """Получить базовые свойства товара, прим. Артикул / Серия.

        Returns:
            dict: Словарь, вида `Наименование свойства`: `Значение свойства`
        """
        props_ul = props_block.find("ul", {"class": "element-property"})
        props_elements = props_ul.find_all("li")
        result = {}
        for element in props_elements:
            title_block = element.find("div", {"class": "name-val"})
            value_block = element.find("div", {"class": "value-val"})
            title = title_block.find("span").text
            value = value_block.find("span").text
            result[title] = value
        return result
    
    def _get_price(self, value):
        # Удаляем пробелы из строки цены
        value = value.replace(" ", "")
        try:
            return Decimal(value)
        except ValueError:
            raise TypeError("Товар не содержит цены")
    
    def _clear(self, value: str) -> str:
        """Удалить пробельные символы в строке.

        Args:
            value (str): Строка, содержащая пробельные символы

        Returns:
            str: Строка, которая не содержит пробельных символов
        """
        return value.replace("\n", "").replace("\t", "")
    
    def _import_product(self, dict: dict) -> Product:
        product = Product.get_instance_by_id(dict['id'])
        product.insert_fields(dict)
        print(product.title)
