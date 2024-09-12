from django.contrib import admin

from .models import Webhook
# Register your models here.

class WebhookAdmin(admin.ModelAdmin):
    readonly_fields=['api_key','secret_key']
    list_display = ['__str__','Management','activated']
    search_fields = ['id','api_key','secret_key']
    
admin.site.register(Webhook,WebhookAdmin)