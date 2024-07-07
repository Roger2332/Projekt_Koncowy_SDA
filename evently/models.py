from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class CreateUserModel(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(unique=True, max_length=50)


class Category(models.Model):
    name = models.CharField(max_length=100)
    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'


class Status(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Rejected', 'Rejected')

    ]
    name = models.CharField(choices=STATUS_CHOICES, max_length=50, default=STATUS_CHOICES[1][0])
    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'


class Event(models.Model):
    author = models.ForeignKey(CreateUserModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    start_at = models.DateField()
    end_at = models.DateField()
    description = models.TextField()
    status = models.ForeignKey(Status, on_delete=models.CASCADE, default=1)
    category = models.ManyToManyField(Category, related_name='events_category', blank=True)
    participants = models.ManyToManyField(CreateUserModel, related_name='events_participated', blank=True)
    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'Event: {self.name}, start at: {self.start_at}, end at: {self.end_at}'
    # dla panelu administratora(żeby poprawnie wyswietliwało się many-to-many)
    def category_list(self):
        return "".join([category.name for category in self.category.all()])
    category_list.short_description = 'Category'


class Comment(models.Model):
    author = models.ForeignKey(CreateUserModel, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    content = models.TextField()
    event_date = models.DateTimeField(auto_now_add=True)
    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'Author: {self.author}, Event: {self.event}'