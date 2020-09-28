from django.contrib import admin

# Register your models here.
from home.models import Users


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in Users._meta.fields
    ]
