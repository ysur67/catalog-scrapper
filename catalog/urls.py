from django.urls import path, include
from catalog.views import (AttributeValueExportView, ProductExportView,
                           ProductFileExportView, ProductImageExportView)


urlpatterns = [
    path("export/", include([
        path("product/", ProductExportView.as_view()),
        path("attributes/", AttributeValueExportView.as_view()),
        path("product-images/", ProductImageExportView.as_view()),
        path("product-files/", ProductFileExportView.as_view())
    ])),
]
