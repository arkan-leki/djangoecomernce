from django.contrib import admin
from django.utils.html import mark_safe
from .models import Collection, Category, Product

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'get_image', 'description_summary')  # Display fields in the list view
    search_fields = ('name', 'slug')  # Search by name and slug
    prepopulated_fields = {'slug': ('name',)}  # Automatically fill the slug field based on the name
    list_filter = ('name',)  # Add filters for the list view
    filter_horizontal = ('products',)  # Add a horizontal filter for selecting related products

    def description_summary(self, obj):
        return obj.description[:50] + "..." if obj.description else "No description"
    description_summary.short_description = 'Description'

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" />')
        return 'No Image'
    get_image.short_description = 'Image'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'get_image')  # Display fields in the list view
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" />')
        return 'No Image'
    get_image.short_description = 'Image'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'brand', 'get_image')  # Display fields in the list view
    search_fields = ('title', 'category__name', 'brand')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('category', 'brand', 'price')

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" />')
        return 'No Image'
    get_image.short_description = 'Image'
