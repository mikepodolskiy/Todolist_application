from django.contrib import admin

from bot.models import TgUser


class TgUserAdmin(admin.ModelAdmin):
    list_display = ("tg_chat_id", "user")
    search_fields = ("tg_chat_id", "username")
    readonly_fields = ("verification_code", )


admin.site.register(TgUser, TgUserAdmin)