from django.core.management.base import BaseCommand, CommandError
from catalog.models import Product
from catalog.utils import CsvConstructor
from datetime import datetime


class Command(BaseCommand):
    
    def handle(self, *args, **options):
        example_product = Product.objects.first()
        header = example_product.__dict__
        header.pop("_state")
        csv = CsvConstructor(str("jopa"))
        csv.set_header(header.keys())
        csv.set_rows(Product.objects.all().values())
        csv.create_file()
        print(csv.absolute_path)
        