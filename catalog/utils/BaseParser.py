
from bs4 import BeautifulSoup
from catalog.models import Product, Category
import requests
from decimal import Decimal


class BaseParser:
    """Абстрактный класс парсера.
    
    Содержит в себе определение
    базовых методов и полей.

    Если обязательные поля и/или методы не были переопределены
    в дочерних классах, то при инициализации будет поднято исключение.
    """

    URL = ""
    URL_BODY = ""
    PRODUCT_ID_DATA_ATTR = ""
    _soup = None
    _subs = list()
    _product_for_import = dict()
    
    def __init__(self):
        self._soup = self._get_base_soup()
        self._validate_required_fields()
        
    def parse(self):
        """Базовый метод, который обязан иметь каждый дочерний от Base класс."""
        raise NotImplementedError("Метод parse должен быть переопределен")
    
    def get_product_dict(self, product):
        raise NotImplementedError("Метод get_product_dict должен быть переопределен")
    
    def get_soup(self, url):
        """Получить экземпляр BeautifulSoup по переданному урлу.

        Args:
            url (str): Урл

        Returns:
            BeautifulSoup: Инстанс бс4, готовый к парсингу
        """
        request = requests.get(url)
        if request.status_code != 200:
            raise ConnectionError(f"Не был получен ответ по адресу: {url}")
        return BeautifulSoup(request.text)
    
    def get_product_attribute_values(self, product):
        raise NotImplementedError("Метод get_product_attribute_values должен быть переопределен")
    
    def subscribe_for_parsed_product(self, subscriber):
        """Метоод подписки на обновление спаршенного продукта.

        Args:
            subscriber: Объект-подписчик, у которого обязательно
            должен быть определен метод `import_product`
        """
        # Проверяем наличие метода у подписчика
        import_product = getattr(subscriber, "import_product", None)
        if not import_product:
            raise NotImplementedError("Каждый подписчик должен обладать методом import_product!")

        self._subs.append(subscriber)
        
    def _notify(self):
        for subscriber in self._subs:
            subscriber.import_product(self._product_for_import)
    
    def _validate_required_fields(self):
        is_valid = True
        if self.URL is None or self.URL == "":
            is_valid = False
        if self.URL_BODY is None or self.URL_BODY == "":
            is_valid = False
        if self.PRODUCT_ID_DATA_ATTR is None or self.PRODUCT_ID_DATA_ATTR == "":
            is_valid = False
        if self._soup is None:
            is_valid = False
        if self._product_for_import is None:
            is_valid = False
        # Массив subs на момент иницилизации объекта может быть пустым
        # поэтому его пропускаем
            
        if not is_valid:
            raise NotImplementedError("Не все обязательные поля класса были переопределены")
        
    
    def _get_id(self, product):
        id_ = product.attrs.get(self.PRODUCT_ID_DATA_ATTR, None)
        if not id_:
            # Если блок не содержит идентификатора - вернуть новый ид из бд
            return Product.get_next()

        try:
            result = int(id_)
        except ValueError:
            result = Product.get_next()
        
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
    
    def _get_base_soup(self):
        return self.get_soup(self.URL)
    
    def _scrap_product_page(self, href):
        raise NotImplementedError("Метод _scrap_product_page должен быть переопределен")
    
    def _scrap_product_desription(self, item):
        raise NotImplementedError("Метод _scrap_product_desription должен быть переопределен")
    
    def _scrap_product_attribute_value(self, item):
        raise NotImplementedError("Метод _scrap_product_attribute_value должен быть переопределен")
    
    def _scrap_product_files(self, item):
        raise NotImplementedError("Метод _scrap_product_file должен быть переопределен")
    
    def _scrap_images(self, soup):
        raise NotImplementedError("Метод _scrap_images должен быть переопределен")
