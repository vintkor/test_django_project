from django.contrib import admin
from .models import Cart, Item


class ItemInline(admin.TabularInline):
    extra = 0
    model = Item


class CartAdmin(admin.ModelAdmin):
    list_display = [Cart, 'get_count_items', 'get_total_price', 'created', 'updated']
    inlines = [ItemInline]
    list_filter = ['updated']


admin.site.register(Cart, CartAdmin)
