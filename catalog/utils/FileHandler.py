import os
from django.conf import settings
import uuid
from django.core.files.temp import NamedTemporaryFile
from django.core.files import File
import requests


class CustomFile:
    PRODUCT_IMAGES_DIR = settings.MEDIA_ROOT + "/product/"
    PRODUCT_FILES_DIR = settings.MEDIA_ROOT + "/files/"
    
    def __init__(self, href) -> None:
        self._href = href
        request = self._download_file()
        self._temporary_body = self._write_content(request)
        self._name = self._get_file_name(self._href)
        # обновляем _body объекта
        self._temporary_body.flush()
        self._body = File(self._temporary_body, self._name)    
        
    @classmethod
    def remove_product_images(cls):
        for file_name in os.listdir(cls.PRODUCT_IMAGES_DIR):
            cls.remove_file(cls.PRODUCT_IMAGES_DIR + file_name)
            
        for file_name in os.listdir(cls.PRODUCT_FILES_DIR):
            cls.remove_file(cls.PRODUCT_FILES_DIR + file_name)

    @classmethod
    def remove_file(cls, file_path):
        os.remove(file_path)
        
    @property
    def body(self):
        return self._body
    
    def _get_file_name(self, href):
        return str(uuid.uuid4()) + "." + self._get_file_extension(href)
   
    def _download_file(self):
        return requests.get(self._href, stream=True)
    
    def _write_content(self, content):
        temp_file = NamedTemporaryFile(delete=True)
        temp_file.write(content.content)
        return temp_file
    
    def _get_file_extension(self, url):
        # Объясняю ниндзя-код
        # Так как сюда будет приходить только путь к картинке
        # Такие пути имеют вид: /path/to/file/file-name.EXTENSION
        # То, сначала делим путь по "/"
        url = url.split("/")
        # Далее берем последний элемент, так нас интересует только
        # расширение файла
        result = url[-1]
        # Делим его еще раз, только на этот раз точкой
        result = result.split(".")
        # Берем последний элемент - расширение файла
        result = result[-1]
        # TODO: Вот здесь придумать что-то получше, так делать нельзя
        # Если расширение файла > 4 символов,
        # то возрвращаем .pdf
        return result if len(result) < 5 else "pdf"
