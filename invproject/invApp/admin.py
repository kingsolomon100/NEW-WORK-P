from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'name', 'sku', 'user', 'quantity', 'display_price')
    
    # 1. This adds a clickable filter sidebar on the right
    list_filter = ('user',) 
    
    # 2. This adds a search bar at the top to search by username or product details
    search_fields = ('user__username', 'name', 'sku')

    def display_price(self, obj):
        return f"₦{obj.price}"
    display_price.short_description = 'Price'