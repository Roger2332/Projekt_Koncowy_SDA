from django.urls import reverse
from django.utils.html import format_html
from django.contrib import admin
from .models import Status, CreateUserModel, Comment, Category, Event


# Inlajnowe panele
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0  # Ilość pustych formularzy do dodawania nowych komentarzy
    fields = ('event', 'content', 'event_date', 'delete_link')
    readonly_fields = ('event', 'content', 'event_date', 'delete_link',)  # Tylko dla odczytywania

    def delete_link(self, obj):
        delete_url = reverse('admin:%s_%s_delete' % (obj._meta.app_label, obj._meta.model_name), args=[obj.pk])
        return format_html('<a href="{}">Delete</a>', delete_url)
    delete_link.allow_tags = True
    delete_link.short_description = 'Actions'


class EventInline(admin.TabularInline):
    model = Event
    extra = 0  # Ilość pustych formularzy do dodawania nowych wydarzeń
    readonly_fields = ('added', 'modified')  # Tylko dla odczytywania



# Zawartość PA
class CreateUserModelAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'groups')
    inlines = [CommentInline, EventInline] # in-line panele dla komentarzy oraz wydarzeń


class EventAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'author', 'place', 'start_at', 'end_at', 'status', 'category_list', 'added', 'modified')
    search_fields = ('name', 'author', 'place', 'start_at', 'end_at', 'status', 'description')
    list_filter = ('status', 'place', 'start_at', 'end_at')
    ordering = ('-start_at',)
    date_hierarchy = 'start_at'

    # optymizacja BD(JOIN author+status)
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author', 'status')


class StatusAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('added',)
    ordering = ('name',)
    readonly_fields = ('added', 'modified')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author_link', 'author', 'event', 'event_date', 'content', 'added', 'modified')
    search_fields = ('author', 'event', 'event_date', 'content')
    list_filter = ('added', 'modified')

    def author_link(self, obj):
        url = reverse('admin:%s_%s_change' % (obj.author._meta.app_label, obj.author._meta.model_name), args=[obj.author.pk])
        return format_html('<a href="{}">{}</a>', url, obj.author)
    author_link.short_description = 'Author'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'added', 'modified')
    search_fields = ('name',)
    list_filter = ('added', 'modified')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(CreateUserModel, CreateUserModelAdmin)

# Personalizacja panelu administracyjnego
admin.site.site_header = 'Аadministrative panel'
admin.site.site_title = 'Administration'
admin.site.index_title = 'Welcome to the admin area'
