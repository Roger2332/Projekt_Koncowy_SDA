from django.contrib import admin

from evently.models import Event, Status, Comment, Subscription, Category, EventCategory

admin.site.register(Event)
admin.site.register(Status)
admin.site.register(Comment)
admin.site.register(Subscription)
admin.site.register(Category)
admin.site.register(EventCategory)

# Register your models here.
