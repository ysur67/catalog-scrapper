from django.db import models


class Category(models.Model):
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
    title = models.CharField(verbose_name="Наименование", max_length=300)
    
    def __str__(self) -> str:
        return self.title
