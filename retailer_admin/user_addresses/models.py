from django.db import models

from users.models import UserModel


class UserAddressModel(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        UserModel,
        models.CASCADE,
        verbose_name="Клиент",
        related_name="addresses",
        blank=False,
        null=False,
    )
    city = models.CharField(
        verbose_name="Город", null=False, blank=False, max_length=32
    )
    street = models.CharField(
        verbose_name="Улица", null=False, blank=False, max_length=32
    )
    house = models.CharField(verbose_name="Дом", null=False, blank=False, max_length=32)
    entrance = models.IntegerField(verbose_name="Подъезд", null=False, blank=False)
    floor = models.IntegerField(verbose_name="Этаж", null=True, blank=True)
    flat = models.CharField(
        verbose_name="Квартира", null=True, blank=True, max_length=32
    )

    def __str__(self):
        return f"{self.city}, {self.street}, {self.house}"

    class Meta:
        managed = False
        db_table = "user_addresses"
        verbose_name = "Адрес клиента"
        verbose_name_plural = "Адреса клиентов"
