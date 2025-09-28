from django.contrib import admin
from django.contrib.auth import get_user_model
from shop.models import Category, Product, ProductImage, Comment, CartItem, Like
from import_export.admin import ImportExportModelAdmin
# Register your models here.

User = get_user_model()
namespace = 'shop'

# admin.site.register(Category)
# admin.site.register(Product)
admin.site.register(Comment)
admin.site.register(CartItem)
admin.site.register(Like)



class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'avg_rating')
    list_filter = ('category', 'price', 'created_at')
    inlines = [ProductImageInline]

@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin ,admin.ModelAdmin):
    list_display = ['title', 'slug']

    prepopulated_fields = {'slug': ('title',)}




admin.site.site_header = 'Admin'
admin.site.site_title = 'Admin'
admin.site.index_title = 'Welcome to Honey Kitchen'
