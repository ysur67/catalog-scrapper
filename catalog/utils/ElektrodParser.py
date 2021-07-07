from catalog.models import attribute
from .BaseParser import BaseParser
from .FileHandler import CustomFile


class ElektrodParser(BaseParser):
    URL = "http://elektrod.ru/esab/?page=equipment"
    URL_BODY = "http://elektrod.ru/esab/"
    
    PRODUCT_ID_DATA_ATTR = "NONE"
    
    def parse(self):
        # Крайне древняя верстка на сайте,
        # потому делаем такие уровни вложенности,
        # чтобы избежать попадания рандомных тегов в требуемые
        for table in self._get_tables():
            table_rows = table.find_all("tr")
            for row in table_rows:
                table_tds = row.find_all("td", "link-description")
                for td in table_tds:
                    self._product_for_import = self._get_product_dict(td)
                    if self._product_for_import is None:
                        continue
                    self._notify()
                    
    def _get_tables(self):
        return self._soup.find_all("table", {"class": "index-gallery"})
    
    def _get_product_dict(self, product):
        id_ = self._get_id(product)
        title_block = product.find("a")
        href = title_block.attrs.get("href")

        if len(href) < 2:
            return None
        
        title = self._clear(title_block.text)

        result = self._scrap_product_page(href)
        result["id"] = id_
        result["title"] = title
        result["price"] = 0
        result["code"] = "ND"
        result["series"] = "ND"
        for key in result:
            print(key)
            print(result[key])
        return result
        
    def _scrap_product_page(self, href):
        soup = self.get_soup(href)
        right_part = soup.find("div", {"class": "right"})
        subparts = right_part.find_all("h5")
        for item in subparts:
            if "Описание" in item.text:
                description = self._scrap_product_desription(item)
                continue
            if "Технические характеристики" in item.text:
                table = soup.find("table", {"class", "item"})
                attribute_values = self._scrap_product_attribute_value(table)
                continue
            if "Инструкции по эксплуатации" in item.text:
                # Таблица с файлами - единственная таблица без
                # класса, поэтому указываем пустой класс
                table = soup.find("table", {"class": ""})
                files = self._scrap_product_files(table)
                continue
            
        images = self._scrap_images(soup)
        result = {}
        result["description"] = description
        result["attribute_values"] = attribute_values
        result["files"] = files
        result["images"] = images
        return result

    def _scrap_product_desription(self, item):
        return self.__construct_product_description(item)
        
    def __construct_product_description(self, item, result_string=""):
        """Рекурсивно создать описание товара."""
        next_element = item.next_sibling
        if next_element is None:
            return result_string
        # Все блоки, до блока технических харакетистик пойдут для описания товара
        # Поэтому останавливаемся только, когда наткнемся на блок хар-тик
        if "Технические характеристики" in self._clear(str(next_element.string)):
            return result_string
        result_string += str(next_element)
        return self.__construct_product_description(next_element, result_string=result_string)

    def _scrap_product_attribute_value(self, item):
        attribute_values = dict()
        for item in item.find_all("tr"):
            td_list = item.find_all("td")
            block_title = td_list[0]
            if len(td_list) == 1:
                block_value = "ND"
            else:
                block_value = td_list[1].text
            title = self._clear(block_title.text)
            value = self._clear(block_value)
            attribute_values[title] = value
        return attribute_values
    
    def _scrap_images(self, soup):
        div_images = soup.find("div", {"class": "left"})
        scraped_images = list()
        for img_block in div_images.find_all("img"):
            href = img_block.attrs.get("src", "")
            image = CustomFile(href=self.URL_BODY + href)
            scraped_images.append(image.body)
        return scraped_images
    
    def _scrap_product_files(self, item):
        downloaded_files = list()
        hyperlinks = item.find_all("a", {"class": ""})
        for link in hyperlinks:
            # скипаем все пустые ссылки
            if link is None:
                continue
            href = link.attrs.get("href")
            # Сначала скипаем а без ссылки
            # Потом, скипаем а, где ссылка #
            # Затем, скипаем а, где нет 'pdf'
            if href is None or len(href) < 2 or "pdf" not in href:
                continue
            file_ = CustomFile(href=self.URL_BODY + href)
            downloaded_files.append(file_.body)

        return downloaded_files
