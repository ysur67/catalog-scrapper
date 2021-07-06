from django.db import models
from .category import Category


class Product(models.Model):
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
    
    title = models.CharField(verbose_name="Наименование", max_length=300)
    code = models.CharField(verbose_name="Артикул", max_length=150, null=True, blank=True)
    series = models.CharField(verbose_name="Серия", max_length=150, null=True, blank=True)
    price = models.DecimalField(verbose_name="Цена", max_digits=12, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория", null=True, blank=True)
    
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
        return cls.objects.last().id + 1

    def insert_fields(self, fields: dict):
        """Заполнить поля товара из переданног словаря.

        Args:
            obj (Proudct): Инстанс модели
            fields (dict): Словарь полей
        """
        self.__dict__.update(fields)
        self.save()
