from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .forms import *
from .models import *


# Register your models here.
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreateForm
    list_display = ('email', 'username', 'full_name', 'is_admin', 'is_superuser',)
    list_filter = ('email', 'is_admin')
    fieldsets = (
        ('user', {'fields': ('email', 'password', 'first_name', 'last_name',)}),
        ('personal info', {'fields': ('is_active', 'is_admin', 'is_superuser',)}),
        # ('Permissions', {'fields': ('groups',)}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'username', 'first_name', 'last_name', 'password1', 'password2')}),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.register(Address)
admin.site.unregister(Group)
