from django.db import models
from .product import Product


class AttributeValue(models.Model):

    class Meta:
        verbose_name = "Атрибут значение"
        verbose_name_plural = "Атрибуты и их значения"

    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                verbose_name="Товар", related_name="attributes")
    title = models.CharField(max_length=300, verbose_name="Наименование")
    value = models.CharField(max_length=300, verbose_name="Значение")
    
    def __str__(self) -> str:
        return f"Значение атрибута {self.title}"
