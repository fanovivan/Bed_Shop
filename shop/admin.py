from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "is_available", "created_at")
    list_filter = ("category", "is_available")
    search_fields = ("name", "description")
    list_editable = ("is_available", "price")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("category", "name", "description", "price", "image")}),
        ("Статус", {"fields": ("is_available",)}),
        (
            "Служебная информация",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )
