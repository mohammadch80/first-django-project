from django.contrib import admin
from .models import Students, Group


# Register your models here.

class StudentInline(admin.StackedInline):
    model = Students
    extra = 1


class StudentsAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Personal", {"fields": ["name", "age"]}),
        ("Education", {"fields": ["score", "group"]})
    ]
    list_display = ["name", "score", "get_rank_in_group"]
    list_filter = ["age"]
    search_fields = ['name']


class GroupAdmin(admin.ModelAdmin):
    inlines = [StudentInline]


admin.site.register(Students, StudentsAdmin)
admin.site.register(Group, GroupAdmin)
