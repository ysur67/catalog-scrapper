from django.db import models


class Category(models.Model):
    title = models.CharField(verbose_name="Наименование", max_length=300)
    
    def __str__(self) -> str:
        return self.title
