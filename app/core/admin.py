"""
Django Admin
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from core import models


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    """Definingthe admin for users."""
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (_('Permissions'), {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }),

        (_('Important dates'), {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser',
            ),
        }),
    )

    readonly_fields = ['last_login']


admin.site.register(models.EthnicGroup)
admin.site.register(models.Tag)
admin.site.register(models.Culture)
admin.site.register(models.Event)
admin.site.register(models.EventImages)
admin.site.register(models.Chief)
admin.site.register(models.Publisher)
admin.site.register(models.Site)
admin.site.register(models.SiteImages)
