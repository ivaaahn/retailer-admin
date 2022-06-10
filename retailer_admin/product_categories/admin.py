from django.contrib import admin

from product_categories.models import ProductCategoryModel
from products.models import ProductModel


class ProductInlineAdmin(admin.TabularInline):
    model = ProductModel
    verbose_name = "Продукт данной категории"
    verbose_name_plural = "Продукты данной категории"
    fields = (
        "name",
        "description",
        "photo_preview",
    )
    readonly_fields = (
        "name",
        "photo_preview",
        "description",
    )
    can_delete = False

    def photo_preview(self, obj):
        return obj.photo_preview

    photo_preview.short_description = "Фото продукта"
    photo_preview.allow_tags = True

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("category")


@admin.register(ProductCategoryModel)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    inlines = (ProductInlineAdmin,)
