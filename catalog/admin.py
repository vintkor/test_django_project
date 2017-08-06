from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import CatalogCategory, CatalogComment, CatalogCurrency, CatalogImage, CatalogProduct, ProductFeature
from feature.models import Feature
from import_export.admin import ImportExportActionModelAdmin


class CatalogCommentInline(admin.StackedInline):
    extra = 0
    model = CatalogComment
    suit_classes = 'suit-tab suit-tab-comment'


class CatalogImageInline(admin.StackedInline):
    extra = 0
    model = CatalogImage
    suit_classes = 'suit-tab suit-tab-image'


class FeatureInline(admin.TabularInline):
    extra = 0
    model = ProductFeature
    suit_classes = 'suit-tab suit-tab-feature'


class CatalogProductAdmin(ImportExportActionModelAdmin):
    list_display = ["title", "category", "active", "price", "currency", "unit", "step", "get_count_comments", "created", "updated"]
    list_filter = ["active", "category"]
    search_fields = ['title']
    prepopulated_fields = {"slug": ("title",)}
    inlines = [CatalogCommentInline, CatalogImageInline, FeatureInline]
    fieldsets = [
        (None, {
            'classes': ('suit-tab', 'suit-tab-product',),
            'fields': ["title", "slug", "category", "price", "currency", "unit", "step", "description", "text", "image", "active"]
        }),
    ]

    suit_form_tabs = (('product', 'Товар'), ('comment', 'Комментарии'), ('image', 'Изображения'), ('feature', 'Характеристика'))
    resource_class = CatalogProduct


class CatalogCommentAdmin(admin.ModelAdmin):
    list_display = ["parent", "created", "updated"]


class CatalogImageAdmin(admin.ModelAdmin):
    list_display = ["parent", "show_image", "active"]


class CatalogCurrencyAdmin(admin.ModelAdmin):
    list_display = ["title", "short_title", "code", "course", "is_main"]


admin.site.register(CatalogCurrency, CatalogCurrencyAdmin)
admin.site.register(CatalogProduct, CatalogProductAdmin)
admin.site.register(CatalogComment, CatalogCommentAdmin)
admin.site.register(CatalogImage, CatalogImageAdmin)
admin.site.register(
    CatalogCategory,
    DraggableMPTTAdmin,
    list_display=('tree_actions', 'indented_title', 'get_count_product', 'show_image', 'active'),
    list_display_links=('indented_title',),
    prepopulated_fields={"slug": ("title",)},
)
