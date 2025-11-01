from django.contrib import admin
from django.contrib import admin
from .models import Task

# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'completed', 'created']
    list_filter = ['completed', 'created']
    search_fields = ['title', 'description']