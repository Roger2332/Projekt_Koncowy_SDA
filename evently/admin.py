from django.contrib import admin
from .models import Category, CreateUserModel, Status

# Register your models her
admin.site.register(Category)
admin.site.register(CreateUserModel)
admin.site.register(Status)