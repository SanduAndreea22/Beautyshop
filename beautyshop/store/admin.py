from django.contrib import admin
from .models import Product, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'category', 'price', 'stock', 'featured', 'rating_avg', 'image_preview')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description', 'brand')
    list_filter = ('category', 'featured', 'stock', 'price')
    readonly_fields = ('rating_avg', 'image_preview')  # rating-ul se calculează automat

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="60" height="60" style="object-fit:cover;border-radius:5px;" />'
        return "-"
    image_preview.allow_tags = True
    image_preview.short_description = 'Image'

    # Opțional: ordonează după rating
    ordering = ('-rating_avg', '-created_at')


