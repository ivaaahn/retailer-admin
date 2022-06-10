from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError

from order.models import OrderModel
from shops.models import ShopModel
from user_addresses.models import UserAddressModel

UserModel = get_user_model()


class ShopInlineAdmin(admin.TabularInline):
    model = ShopModel.staff.through
    verbose_name = "Магазин"
    verbose_name_plural = "Магазины"
    extra = 0
    raw_id_fields = ("shop",)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "shop":
            kwargs["queryset"] = ShopModel.objects.select_related("address").all()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class AddressInlineAdmin(admin.StackedInline):
    model = UserAddressModel
    extra = 0


class OrderInlineAdmin(admin.StackedInline):
    model = OrderModel
    readonly_fields = ("total_price", "created_at", "receive_kind", "status")
    fields = ("total_price", "created_at", "receive_kind", "status")
    show_change_link = True
    verbose_name = "Заказ"
    verbose_name_plural = "Заказы"
    extra = 0
    can_delete = False
    # raw_id_fields = ("shop", "address")

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("user", "shop", "address")
            .prefetch_related("products")
        )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "shop":
            kwargs["queryset"] = ShopModel.objects.select_related("address").all()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput({"autocomplete": "Новый пароль"}),
        strip=False,
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput({"autocomplete": "Новый пароль"}),
        strip=False,
    )

    class Meta:
        model = UserModel
        fields = ("email", "name", "is_active", "role")

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = (
            "email",
            "name",
            "birthday",
            "is_active",
            "role",
            "groups",
        )


class GroupInlineAdmin(admin.TabularInline):
    model = UserModel.groups.through
    verbose_name = "Группа пользователя"
    verbose_name_plural = "Группы пользователя"
    extra = 0


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = (
        "name",
        "email",
        "role",
        "is_active",
    )
    list_filter = ("role",)
    fieldsets = (
        (
            "Личная информация",
            {
                "fields": (
                    "name",
                    "email",
                    "birthday",
                )
            },
        ),
        (
            "Разрешения",
            {
                "fields": (
                    "role",
                    "is_active",
                )
            },
        ),
    )
    inlines = (
        AddressInlineAdmin,
        ShopInlineAdmin,
        GroupInlineAdmin,
        OrderInlineAdmin,
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.

    add_fieldsets = (
        (
            "Почта и пароль",
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
        (
            "Личная информация",
            {
                "classes": ("wide",),
                "fields": (
                    "name",
                    "birthday",
                ),
            },
        ),
        (
            "Настройки аккаунта",
            {
                "classes": ("wide",),
                "fields": (
                    "role",
                    "is_active",
                ),
            },
        ),
    )
    search_fields = ("email", "name")
    ordering = ("name", "email")
    filter_horizontal = ()


# Create ModelForm based on the Group model.
class GroupAdminForm(forms.ModelForm):
    class Meta:
        model = Group
        exclude = []

    # Add the users field.
    users = forms.ModelMultipleChoiceField(
        queryset=UserModel.objects.all().filter(role="staff"),
        required=False,
        # Use the pretty 'filter_horizontal widget'.
        widget=FilteredSelectMultiple("users", False),
    )

    def __init__(self, *args, **kwargs):
        # Do the normal form initialisation.
        super(GroupAdminForm, self).__init__(*args, **kwargs)
        # If it is an existing group (saved objects have a pk).
        if self.instance.pk:
            # Populate the users field with the current Group users.
            self.fields["users"].initial = self.instance.user_set.all()

    def save_m2m(self):
        # Add the users to the Group.
        self.instance.user_set.set(self.cleaned_data["users"])

    def save(self, *args, **kwargs):
        # Default save
        instance = super(GroupAdminForm, self).save()
        # Save many-to-many data
        self.save_m2m()
        return instance


# Create a new Group admin.
class GroupAdmin(admin.ModelAdmin):
    # Use our custom form.
    form = GroupAdminForm
    # Filter permissions horizontal as well.
    filter_horizontal = ["permissions"]


# Register the new Group ModelAdmin.
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)

admin.site.register(UserModel, UserAdmin)
