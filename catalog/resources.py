from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from catalog.models import CatalogProduct, CatalogCategory


class CatalogProductResource(resources.ModelResource):
    category = fields.Field(
        column_name='category',
        attribute='category',
        widget=ForeignKeyWidget(CatalogCategory, 'id')
    )

    class Meta:
        model = CatalogProduct
