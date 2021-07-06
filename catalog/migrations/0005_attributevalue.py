# Generated by Django 3.2.5 on 2021-07-06 17:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_product_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttributeValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='Наименование')),
                ('value', models.CharField(max_length=300, verbose_name='Значение')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attributes', to='catalog.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Атрибут значение',
                'verbose_name_plural': 'Атрибуты и их значения',
            },
        ),
    ]
