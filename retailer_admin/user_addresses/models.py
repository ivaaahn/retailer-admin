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
    city = models.TextField(verbose_name="Город", null=False, blank=False)
    street = models.TextField(verbose_name="Улица", null=False, blank=False)
    house = models.TextField(verbose_name="Дом", null=False, blank=False)
    entrance = models.IntegerField(verbose_name="Подъезд", null=False, blank=False)
    floor = models.IntegerField(verbose_name="Этаж", null=True, blank=True)
    flat = models.CharField(
        verbose_name="Квартира", null=True, blank=True, max_length=6
    )

    def __str__(self):
        return f"{self.city}, {self.street}, {self.house}"

    class Meta:
        managed = False
        db_table = "user_addresses"
        verbose_name = "Адрес клиента"
        verbose_name_plural = "Адреса клиентов"
