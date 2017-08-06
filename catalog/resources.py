from import_export.resources import ModelResource
from catalog.models import CatalogProduct


class CatalogProductResource(ModelResource):

    class Meta:
        model = CatalogProduct
