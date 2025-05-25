from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Product, Comment  # ← импорт Comment

@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name', )

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'product', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('author', 'text')