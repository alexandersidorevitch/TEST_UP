from django.contrib import admin

# Register your models here.
from account.models import TestResult


def to_note_the_results(modeladmin, request, queryset):
    queryset.update(checked=True)


def cancel_to_note_the_results(modeladmin, request, queryset):
    queryset.update(checked=False)


# Action description
to_note_the_results.short_description = "Отметить те результаты, которые занесены в журнал"
cancel_to_note_the_results.short_description = "Отметить те результаты, которые не занесены в журнал"


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in TestResult._meta.fields
    ]
    list_filter = ('user', 'topic', 'checked')
    date_hierarchy = 'data'
    search_fields = ['user__username']
    actions = [to_note_the_results, cancel_to_note_the_results]


admin.site.site_header = 'Тестирующая система'
