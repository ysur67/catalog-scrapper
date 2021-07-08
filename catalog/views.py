from catalog.models.images import ProductImage
from catalog.utils.CsvCreator import CsvConstructor
from django.http.response import Http404, HttpResponse
from django.shortcuts import render
from django.views import View
from catalog.models import Product, AttributeValue
from datetime import datetime


class BaseExportView(View):
    MODEL_CLASS = ""
    CSV_CONSTRUCTOR_CLASS = CsvConstructor
    
    def get(self, request, *args, **kwargs):
        example_product = self.MODEL_CLASS.objects.first()
        if not example_product:
            return Http404()

        header = example_product.__dict__
        header.pop("_state")
        row_data = self.MODEL_CLASS.objects.all().values()
        file_name = self._generate_file_name()
        csv = self.CSV_CONSTRUCTOR_CLASS(file_name)
        csv.set_header(header)
        csv.set_rows(rows=row_data)
        csv.create_file()
        file_path = csv.absolute_path
        with open(file_path, 'r') as f:
            file_data = f.read()
        response = HttpResponse(file_data, content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = f"attachment; filename={csv.name}"
        return response
        
    def _generate_file_name(self):
        file_name = self.MODEL_CLASS.objects.model._meta.db_table
        file_name += datetime.now().strftime("%d_%B_%Y")
        return file_name

class ProductExportView(BaseExportView):
    MODEL_CLASS = Product
    
class AttributeValueExportView(BaseExportView):
    MODEL_CLASS = AttributeValue

class ProductImageExportView(BaseExportView):
    MODEL_CLASS = ProductImage
