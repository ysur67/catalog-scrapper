from .BaseParser import BaseParser
from .FileHandler import CustomFile


class FoxweldParser(BaseParser):
    """Класс парсера сайта foxweld.ru."""

    URL = "https://foxweld.ru/products/elektrosvarka/"
    URL_BODY = "https://foxweld.ru"
    PRODUCT_ID_DATA_ATTR = "data-id"

    def parse(self):
        last_page = self._get_last_page()
        for page in range(1, last_page):
            self._scrap_page(page)
        
    def _get_last_page(self):
        pagination_block = self._soup.find("div", {"class": "modern-page-navigation"})
        pagination_links = pagination_block.find_all("a")
        pages = list()
        for link in pagination_links:
            value = link.text
            try:
                value = int(value)
            except ValueError:
                value = 0
            pages.append(value)
        return max(pages)
    
    def _scrap_page(self, page_number):
        pagin_url = self.URL + f"?PAGEN_1={page_number}"
        soup = self.get_soup(pagin_url)
        items = soup.find_all("li", {"class": "item"})
        for item in items:
            # Изменяем словарь класса на новый словарь
            self._product_for_import = self._get_product_dict(item)
            # Уведомляем подписчиков о смене словаря
            self._notify()

    def _get_product_dict(self, product):
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
        # Если карточка товара не содержит его стоимости
        # То даем ей значение строковое значение 0,
        # Для последующей конвертации в целочисленное значение 0
        if price_block:
            price_value = price_block.find("b").text
        else:
            price_value = "0"
        
        product_title = self._clear(title_block.text)
        product_price = self._clear(price_value)
        for key in product_props:
            product_props[key] = self._clear(product_props[key])
        
        href = title_block.find("a").attrs.get("href", None)
        result = self._scrap_product_page(href)
        result['id'] = id_
        result['title'] = product_title
        result['price'] = self._get_price(product_price)
        result['code'] = product_props.get("Артикул:", None)
        result['series'] = product_props.get("Серия:", None)
        
        for key in result:
            print(key)
            print(result[key])
        return result
    
    def _get_props(self, block):
        """Получить базовые свойства товара со страницы списка, прим. Артикул / Серия.

        Returns:
            dict: Словарь, вида `Наименование свойства`: `Значение свойства`
        """
        props_ul = block.find("ul", {"class": "element-property"})
        props_elements = props_ul.find_all("li")
        result = {}
        for element in props_elements:
            title_block = element.find("div", {"class": "name-val"})
            value_block = element.find("div", {"class": "value-val"})
            title = title_block.find("span").text
            value = value_block.find("span").text
            result[title] = value
        return result
        
    def _scrap_product_page(self, href) -> dict:
        soup = self.get_soup(self.URL_BODY + href)
        product_info_blocks = soup.find_all("div", {"class": "tab-view-content"})
        description = ""
        attribute_values = {}
        files = list()
        for block in product_info_blocks:
            block_name = block.attrs.get("id", None)
            if "detail" in block_name:
                description = self._scrap_product_desription(block)
                continue
            if "properties" in block_name:
                attribute_values = self._scrap_product_attribute_value(block)
                continue
            if "download" in block_name:
                files = self._scrap_product_files(block)
                continue
        images = self._scrap_images(soup)
        result = {}
        result["description"] = description
        result["attribute_values"] = attribute_values
        result["files"] = files
        result["images"] = images
        return result
    
    def _scrap_product_desription(self, item):
        # .decode_contents()
        # https://tedboy.github.io/bs4_doc/generated/generated/bs4.BeautifulSoup.decode_contents.html
        return item.find("div", {"class": "i-block-content"}).decode_contents()
    
    def _scrap_product_attribute_value(self, item):
        content_block = item.find("div", {"class": "i-block-content"})
        ul = content_block.find("ul")
        # В список li, летят какие-то рандомные li с классом
        # Чтобы от них избавиться добавляем, что класс должен быть пустым
        list_ = ul.find_all("li", {"class": ""})
        attribute_values = dict()
        for li in list_:
            block_title = li.find("div", {"class": "name-val"})
            block_value = li.find("div", {"class": "value-val"})
            span_title = block_title.find("span")
            span_value = block_value.find("span")
            title = self._clear(span_title.text)
            value = self._clear(span_value.text)
            attribute_values[title] = value
        return attribute_values
    
    def _scrap_product_files(self, item):
        li_files = item.find_all("li", {"class", "dwl-pdf"})
        downloaded_files = list()
        for li in li_files:
            hyperlink = li.find("a")
            href = hyperlink.attrs.get("href")
            file_ = CustomFile(href=href)
            downloaded_files.append(file_.body)
        return downloaded_files
    
    def _scrap_images(self, soup):
        div_images = soup.find_all("div", {"class": "image"})
        downloaded_images = list()
        for div in div_images:
            image = div.find("a", {"class": "fancy"})
            if image is None:
                continue
            href = image.attrs.get("href", "")
            image = CustomFile(href=self.URL_BODY + href)
            downloaded_images.append(image.body)

        return downloaded_images
