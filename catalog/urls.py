from django.urls import path
from catalog.views import AttributeValueExportView, ProductExportView, ProductImageExportView


urlpatterns = [
    path("export/product/", ProductExportView.as_view()),
    path("export/attribute/", AttributeValueExportView.as_view()),
    path("export/images/", ProductImageExportView.as_view()),
]
