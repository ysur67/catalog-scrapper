from django.db import models
from .product import Product


class ProductFile(models.Model):
    
    class Meta:
        verbose_name = "Файл"
        verbose_name_plural = "Файлы"
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                verbose_name="Товар", related_name="files")
    file = models.FileField(upload_to="files")

    def __str__(self) -> str:
        return f"Загружаемый файл товара {self.product.title}"
