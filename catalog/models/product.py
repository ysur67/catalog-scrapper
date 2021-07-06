from django.db import models


class Product(models.Model):
    title = models.CharField(verbose_name="Наименование", max_length=300)
    code = models.CharField(verbose_name="Артикул", max_length=150)
    price = models.DecimalField(verbose_name="Цена", max_digits=12, decimal_places=2)
    
    def __str__(self) -> str:
        return self.title
