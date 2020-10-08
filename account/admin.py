from django.contrib import admin

# Register your models here.
from account.models import TestResult


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in TestResult._meta.fields
    ]
