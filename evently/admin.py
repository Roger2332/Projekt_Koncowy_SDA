from django.contrib import admin
from django.utils.html import format_html
from .models import CreateUserModel, Event, Comment, Category


class CreateUserModelAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'groups')
    ordering = ('username',)


class EventAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'author', 'place', 'start_at', 'end_at', 'status', 'category', 'description', 'added', 'modified')
    search_fields = ('name', 'author', 'place', 'start_at', 'end_at', 'status', 'description')
    list_filter = ('status', 'place', 'start_at', 'end_at')
    ordering = ('-start_at',)
    date_hierarchy = 'start_at'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'added', 'modified')
    search_fields = ('name',)
    list_filter = ('added', 'modified')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'event', 'event_date', 'content', 'added', 'modified')
    search_fields = ('author', 'event', 'event_date', 'content')
    list_filter = ('added', 'modified')

admin.site.register(CreateUserModel, CreateUserModelAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)

# Персонализация панели администратора
admin.site.site_header = 'Аadministrative panel'
admin.site.site_title = 'Administration'
admin.site.index_title = 'Welcome to the admin area'