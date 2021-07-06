from django.db import models 
from .product import Product
from django.conf import settings


class ProductImage(models.Model):
    
    class Meta:
        verbose_name = "Картинка товара"
        verbose_name_plural = "Картинки товаров"
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                verbose_name="Товар", related_name="images",)
    image = models.ImageField()
    
    def __str__(self) -> str:
        return f"Картинка товара {self.product.title}"
