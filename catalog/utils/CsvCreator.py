import csv
from django.conf import settings
from django.db.models import fields


class CsvConstructor:
    
    DEFAULT_FILE_PATH = settings.MEDIA_ROOT + "/csv/"

    def __init__(self, file_name: str) -> None:
        """Инициализация конструктора файла.

        Args:
            file_name (str): Имя для файла
        """
        self._header = list()
        self._rows = dict()
        self._is_created = False
        self._name = file_name + ".csv"
        self._delimiter = ";"
        
    def set_delimiter(self, value: str):
        """Установить сепаратор в .csv файле.

        Args:
            value (str): Символ сепаратора

        Raises:
            ValueError: Если длина строки больше 1
        """
        if len(value) > 1:
            raise ValueError("Размер сепаратора не может быть больше 1 символа")
        self._delimiter = value

    def set_header(self, header: dict):
        """Настроить оглавленеие файла."""
        self._header = header

    def set_rows(self, rows: list):
        """Передать массив, которым будет заполнен csv файл."""
        self._rows = rows

    def create_file(self):
        """Создать файл и заполнить его переданной информацией."""
        if not self._header:
            raise AttributeError("Файл не может быть создан без оглавления")
        if not self._rows:
            raise AttributeError("Файл не может быть создан без строк")
        
        file_ = open(self.DEFAULT_FILE_PATH + self._name, 'w+', encoding='UTF8', newline="")
        
        writer = csv.DictWriter(file_, fieldnames=self._header, delimiter=self._delimiter)
        writer.writeheader()
        writer.writerows(self._rows)

        file_.close()
        self._is_created = True

    @property
    def absolute_path(self):
        """Абсолютный путь до созданного файла в системе."""
        if not self._is_created:
            raise FileNotFoundError("Невозможно получить путь файла до его создания")
        return self.DEFAULT_FILE_PATH + self._name

    @property
    def name(self):
        return self._name
