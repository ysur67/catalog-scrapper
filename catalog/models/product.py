from django.db import models
from django.db.models.fields import BLANK_CHOICE_DASH
from django.utils.text import slugify
from .category import Category
from ckeditor.fields import RichTextField


class Product(models.Model):
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
    
    title = models.CharField(verbose_name="Наименование", max_length=300)
    code = models.CharField(verbose_name="Артикул", max_length=150, null=True, blank=True)
    series = models.CharField(verbose_name="Серия", max_length=150, null=True, blank=True)
    price = models.DecimalField(verbose_name="Цена", max_digits=12, decimal_places=2)
    category = models.CharField(verbose_name="Категория", max_length=300, blank=True, null=True)
    description = RichTextField(verbose_name="Описание", null=True, blank=True)
    slug = models.SlugField(max_length=300, verbose_name="Символьный код", null=True, blank=True)
    image = models.ImageField(upload_to="product", null=True, blank=True)
    
    def __str__(self) -> str:
        return self.title
    
    @classmethod
    def get_instance_by_id(cls, id):
        """Получить инстанс по ИД.

        Если инстанса с таким ИД не существует, то вернется новый,
        у которого еще не вызывался метод `save`

        Args:
            id (int): ИД

        Returns:
            Product: Инстанс модели
        """
        qs = cls.objects.filter(id=id)
        if qs.exists():
            return qs.first()
        
        return cls(id=id)

    @classmethod
    def get_next(cls) -> int:
        """Получить ид последнего продукта + 1.

        Returns:
            int: ID
        """
        last_obj = cls.objects.last()
        
        if last_obj is None:
            return 1
        
        return last_obj.id + 1

    def insert_fields(self, fields: dict):
        """Заполнить поля товара из переданног словаря.

        Args:
            obj (Proudct): Инстанс модели
            fields (dict): Словарь полей
        """
        self.__dict__.update(fields)
        self.save()

    def update_slug(self):
        self.slug = slugify(self.title)
        self.save()
        
    def upload_image(self, image):
        self.image = image
        self.save()
