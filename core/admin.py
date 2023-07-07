from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group


from core.models import User


class MyAdmin(admin.ModelAdmin):
    list_filter = ("is_staff", "is_active", "is_superuser")
    list_display = ("username", "email", "first_name", "last_name")
    search_fields = ("username", "first_name", "last_name")
    # exclude = ["password"]
    fields = ("username", "first_name", "last_name", "email", "is_staff", "is_active", "last_login", "date_joined")
    readonly_fields = ("last_login", "date_joined")


admin.site.register(User, MyAdmin)
admin.site.unregister(Group)
