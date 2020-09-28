from django.contrib import admin

# Register your models here.
from topic.models import Topics, Answers, Types, Questions


@admin.register(Topics)
class TopicAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in Topics._meta.fields
    ]


class AnswersInline(admin.TabularInline):
    model = Answers
    extra = 0


@admin.register(Types)
class TypesAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in Types._meta.fields
    ]


@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in Questions._meta.fields
    ]
    inlines = [AnswersInline]


@admin.register(Answers)
class AnswersAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in Answers._meta.fields
    ]
