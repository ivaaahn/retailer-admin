from django.db import models
from django.utils.safestring import mark_safe

from product_categories.models import ProductCategoryModel


class ProductModel(models.Model):
    id = models.BigAutoField(verbose_name="Идентификатор", primary_key=True)
    name = models.TextField(verbose_name="Название", null=False, blank=False)
    photo = models.ImageField(
        verbose_name="Фото", null=True, blank=True, upload_to="products/"
    )
    description = models.TextField(verbose_name="Описание", null=True, blank=True)
    category = models.ForeignKey(
        ProductCategoryModel,
        models.CASCADE,
        verbose_name="Категория",
        blank=False,
        null=False,
    )

    @property
    def photo_preview(self):
        if self.photo:
            return mark_safe(
                '<img src="{url}" width="320" height=240 />'.format(
                    url=self.photo.url,
                )
            )
        return ""

    def __str__(self):
        return f"{self.name} / Категория: {self.category}"

    class Meta:
        managed = False
        db_table = "products"
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
