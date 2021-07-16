from catalog.utils.CsvCreator import CsvConstructor
from django.http.response import Http404, HttpResponse
from django.db.models.functions import Concat
from django.shortcuts import render
from django.views import View
from catalog.models import Product, AttributeValue, ProductImage, ProductFile
from datetime import datetime
from catalog.serializers import (ProductFileSerializer, ProductImageSerializer, ProductSerializer,
                                AttributeValueSerializer)


class BaseExportView(View):
    MODEL_CLASS = None
    CSV_CONSTRUCTOR_CLASS = CsvConstructor
    SERIALIZER_CLASS = None
    
    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        if not qs.exists():
            return Http404()
        header = self.SERIALIZER_CLASS.Meta.fields
        row_data = self.SERIALIZER_CLASS(qs, many=True).data
        file_name = self._generate_file_name()
        csv = self.CSV_CONSTRUCTOR_CLASS(file_name)
        csv.set_header(header)
        csv.set_rows(rows=row_data)
        csv.set_delimiter("|")
        csv.create_file()
        file_path = csv.absolute_path
        with open(file_path, 'r') as f:
            file_data = f.read()
        response = HttpResponse(file_data, content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = f"attachment; filename={csv.name}"
        return response
    
    def get_queryset(self):
        return self.MODEL_CLASS.objects.all()
    
    def _generate_file_name(self):
        file_name = self.MODEL_CLASS.objects.model._meta.db_table
        file_name += datetime.now().strftime("%d_%B_%Y")
        return file_name


class ProductExportView(BaseExportView):
    MODEL_CLASS = Product
    SERIALIZER_CLASS = ProductSerializer
    
    
class AttributeValueExportView(BaseExportView):
    MODEL_CLASS = AttributeValue
    SERIALIZER_CLASS = AttributeValueSerializer
    

class ProductImageExportView(BaseExportView):
    MODEL_CLASS = ProductImage
    SERIALIZER_CLASS = ProductImageSerializer


class ProductFileExportView(BaseExportView):
    MODEL_CLASS = ProductFile
    SERIALIZER_CLASS = ProductFileSerializer
