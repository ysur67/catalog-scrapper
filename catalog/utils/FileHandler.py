import os
from django.conf import settings
import uuid


class FileHandler:
    PRODUCT_IMAGES_DIR = settings.MEDIA_ROOT + "/product/"
    
    @classmethod
    def get_tmp_file_path(cls, href):
        file_name = str(uuid.uuid4()) + "." + cls._get_file_extension(href)
        file_path = cls.PRODUCT_IMAGES_DIR + file_name
        return file_path

    @classmethod
    def _get_file_extension(cls, url):
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
        return result[-1]
    
    @classmethod
    def create_file(cls, file_path, content):
        with open(file_path, "wb") as file:
                file.write(content)
                
    @classmethod
    def remove_product_images(cls):
        for file_name in os.listdir(cls.PRODUCT_IMAGES_DIR):
            cls.remove_file(cls.PRODUCT_IMAGES_DIR + file_name)

    @classmethod
    def remove_file(cls, file_path):
        os.remove(file_path)
