from django.core.management.base import BaseCommand, CommandError
from catalog.models import Product, AttributeValue, ProductImage
from catalog.utils import FoxweldParser, FileHandler


class Command(BaseCommand):
    PARSER_CLASSES = (FoxweldParser, )

    def handle(self, *args, **options):
        # Сначала удаляем все картинки, дабы не было дублирования
        ProductImage.objects.all().delete()
        FileHandler.remove_product_images()
        
        for parser_class in self.PARSER_CLASSES:
            parser = parser_class()
            parser.subscribe_for_parsed_product(self)
            parser.parse()
    
    def import_product(self, product_dict: dict) -> Product:
        # Забираем лишние поля из пришедшего словаря
        attribute_values = product_dict.pop("attribute_values")
        files = product_dict.pop("files")
        images = product_dict.pop("images")

        product = Product.get_instance_by_id(product_dict["id"])
        product.insert_fields(product_dict)
        self._import_product_attributes(product, attribute_values)
        self._import_product_images(product, images)

    def _import_product_attributes(self, product: Product, attribute_values: dict):
        for key in attribute_values:
            attribute, _ = AttributeValue.objects.get_or_create(title=key, product=product)
            attribute.value = attribute_values[key]
            attribute.save()
            
    def _import_product_images(self, product, images):   
        for path in images:
            # Ранее везде использовался Path,
            # здесь превращаем его в строку,
            # чтобы джанга его с кайфом схвала
            path = str(path)
            ProductImage.objects.create(product=product, image=path)
