from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import *


class CatalogCommentInline(admin.StackedInline):
    extra = 0
    model = CatalogComment
    suit_classes = 'suit-tab suit-tab-comment'


class CatalogImageInline(admin.StackedInline):
    extra = 0
    model = CatalogImage
    suit_classes = 'suit-tab suit-tab-image'


class CatalogProductAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "active", "price", "currency", "step", "get_count_comments", "created", "updated"]
    list_filter = ["active", "category"]
    search_fields = ['title']
    inlines = [CatalogCommentInline, CatalogImageInline]
    fieldsets = [
        (None, {
            'classes': ('suit-tab', 'suit-tab-product',),
            'fields': ["title", "category", "price", "currency", "step", "description", "text", "active"]
        }),
    ]

    suit_form_tabs = (('product', 'Товар'), ('comment', 'Комментарии'), ('image', 'Изображения'))


class CatalogCommentAdmin(admin.ModelAdmin):
    list_display = ["parent", "created", "updated"]


class CatalogImageAdmin(admin.ModelAdmin):
    list_display = ["parent", "show_image", "is_main", "active"]


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
)
