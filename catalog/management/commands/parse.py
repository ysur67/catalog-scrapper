from catalog.models.files import ProductFile
from django.core.management.base import BaseCommand, CommandError
from catalog.models import Product, AttributeValue, ProductImage, ProductFile
from catalog.utils import FoxweldParser, CustomFile, ElektrodParser


class Command(BaseCommand):
    PARSER_CLASSES = (ElektrodParser, FoxweldParser)

    def handle(self, *args, **options):
        # Сначала удаляем все картинки, дабы не было дублирования
        ProductImage.objects.all().delete()
        CustomFile.remove_product_images()
        # Потом, удаляем все файлы товаров
        ProductFile.objects.all().delete()
        # Далее, удаляем все свойства товара, также чтобы избежать дублирования
        AttributeValue.objects.all().delete()
        
        for parser_class in self.PARSER_CLASSES:
            parser = parser_class()
            parser.subscribe_for_parsed_product(self)
            parser.parse()
            parser.unsubscribe(self)
            
    def on_notify(self, product_dict):
        self.import_product(product_dict)
    
    def import_product(self, product_dict: dict):
        # Забираем лишние поля из пришедшего словаря
        attribute_values = product_dict.pop("attribute_values")
        files = product_dict.pop("files")
        images = product_dict.pop("images")

        product = Product.get_instance_by_id(product_dict["id"])
        product.insert_fields(product_dict)
        self._import_product_attributes(product, attribute_values)
        self._import_product_images(product, images)
        self._import_product_files(product, files)
        
    def _import_product_attributes(self, product: Product, attribute_values: dict):
        for key in attribute_values:
            attribute, _ = AttributeValue.objects.get_or_create(title=key, product=product)
            attribute.value = attribute_values[key]
            attribute.save()
            
    def _import_product_images(self, product, images):   
        for file_body in images:           
            ProductImage.objects.create(product=product, image=file_body)
            
    def _import_product_files(self, product, files):
        if files is None:
            return
        for file_body in files:
            ProductFile.objects.create(product=product, file=file_body)
