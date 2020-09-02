from django.contrib.auth.admin import UserAdmin as BaseAdmin
from django.contrib import admin
from django.contrib import messages
from .models import User
from django.utils.translation import gettext_lazy as _


class UserAdmin(BaseAdmin):
    actions = ['mark_superuser', 'unmark_superuser']
    fieldsets = (
        (None, {'fields': ('student_id', 'password')}),
        (_('Personal info'), {'fields': ('gid', 'nick_name', 'real_name', 'email', 'phone', 'avatar', 'profile')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    ordering = ('nick_name',)
    list_display = ('student_id', 'email', 'nick_name', 'real_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')

    def mark_superuser(self, request, queryset):
        updated = queryset.update(is_superuser=True)
        self.message_user(request, (
            '设置了 %d 名用户为系统管理员。'
        ) % updated, messages.SUCCESS)
    mark_superuser.short_description = "Mark selected users as superuser"  # type: ignore

    def unmark_superuser(self, request, queryset):
        updated = queryset.update(is_superuser=False)
        self.message_user(request, (
            '取消设置了 %d 名用户为系统管理员。'
        ) % updated, messages.SUCCESS)
    unmark_superuser.short_description = "Unmark selected users as superuser"  # type: ignore


admin.site.register(User, UserAdmin)
